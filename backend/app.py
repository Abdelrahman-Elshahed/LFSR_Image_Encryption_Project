import io
import base64
import numpy as np
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import sys
import os
import uuid
from typing import List

# Add parent directory to import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from LFSR_Encryption import LFSRCipher, apply_confusion, apply_diffusion, decrypt_image

app = FastAPI(title="LFSR Encryption API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory cache for encryption parameters
encryption_cache = {}

@app.post("/api/encrypt")
async def encrypt_image_endpoint(
    image: UploadFile = File(...),
    seed: int = Form(...),
    tap_positions: str = Form(...)
):
    """Encrypt an image using LFSR cipher"""
    # Parse tap positions
    tap_positions_list = [int(pos) for pos in tap_positions.split(",")]
    
    # Read and convert image
    image_bytes = await image.read()
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img_array = np.array(img)
    
    # Encrypt image
    encrypted_img, indices = encrypt_image_from_array(img_array, seed, tap_positions_list)
    
    # Convert encrypted image to base64
    encrypted_pil = Image.fromarray(encrypted_img.astype(np.uint8))
    buffer = io.BytesIO()
    encrypted_pil.save(buffer, format="PNG")
    encrypted_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    # Store encryption parameters
    encryption_id = str(uuid.uuid4())
    encryption_cache[encryption_id] = {
        "indices": indices.tolist(),  # Convert numpy array to list for storage
        "seed": seed,
        "tap_positions": tap_positions_list
    }
    
    return {
        "encryption_id": encryption_id,
        "encrypted_image": encrypted_base64
    }

@app.post("/api/decrypt")
async def decrypt_image_endpoint(
    image: UploadFile = File(None),
    encryption_id: str = Form(...),
    encrypted_base64: str = Form(None)
):
    """Decrypt an image using stored encryption parameters"""
    if encryption_id not in encryption_cache:
        raise HTTPException(status_code=404, detail="Encryption parameters not found")
    
    # Get encryption parameters
    params = encryption_cache[encryption_id]
    indices = np.array(params["indices"])
    seed = params["seed"]
    tap_positions = params["tap_positions"]
    
    # Get encrypted image from either file upload or base64
    if image:
        image_bytes = await image.read()
        encrypted_img = np.array(Image.open(io.BytesIO(image_bytes)))
    elif encrypted_base64:
        encrypted_img = np.array(Image.open(io.BytesIO(base64.b64decode(encrypted_base64))))
    else:
        raise HTTPException(status_code=400, detail="Either image file or base64 data required")
    
    # Decrypt image
    decrypted_img = decrypt_image(encrypted_img, indices, seed, tap_positions)
    
    # Convert to base64
    decrypted_pil = Image.fromarray(decrypted_img.astype(np.uint8))
    buffer = io.BytesIO()
    decrypted_pil.save(buffer, format="PNG")
    decrypted_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return {
        "decrypted_image": decrypted_base64
    }

def encrypt_image_from_array(img_array, seed, tap_positions):
    """Helper function to encrypt image from numpy array"""
    # Create LFSR for confusion
    lfsr_confusion = LFSRCipher(seed, tap_positions)
    keystream = lfsr_confusion.generate_keystream(img_array.size)
    
    # Apply confusion
    confused_img = apply_confusion(img_array, keystream)
    
    # Create LFSR for diffusion
    lfsr_diffusion = LFSRCipher(seed ^ 0xA5A5A5, tap_positions)
    
    # Apply diffusion
    encrypted_img, indices = apply_diffusion(confused_img, lfsr_diffusion)
    
    return encrypted_img, indices