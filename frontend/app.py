import streamlit as st
import requests
import io
import base64
from PIL import Image
import numpy as np

# API configuration
API_URL = "http://localhost:8000/api"  # Change to match your FastAPI server

st.set_page_config(
    page_title="LFSR Image Encryption",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("LFSR Image Encryption and Decryption")
st.markdown("""
This application demonstrates image encryption and decryption using Linear Feedback Shift Register (LFSR) cipher
with confusion and diffusion techniques.
""")

# Sidebar for parameters and controls
st.sidebar.title("Encryption Parameters")

# Change from number_input to text_input for seed
seed_text = st.sidebar.text_input(
    "Seed Value (hex)", 
    value="0xB7E15163",
    help="Initial state of LFSR in hexadecimal format (Recommended: 0xB7E15163)"
)

# Convert hex string to integer (safely)
try:
    # Handle both with and without "0x" prefix
    if seed_text.lower().startswith("0x"):
        seed = int(seed_text, 16)
    else:
        seed = int("0x" + seed_text, 16)
except ValueError:
    st.sidebar.error("Please enter a valid hexadecimal value")
    seed = 0xB7E15163  # Default value if input is invalid

tap_positions = st.sidebar.text_input(
    "Tap Positions", 
    value="32,22,2,1",
    help="Comma-separated positions for LFSR feedback (Recommended: 32,22,2,1)"
)

# Information about parameter selection
with st.sidebar.expander("Parameter Recommendations"):
    st.markdown("""
    **Recommended Seed Values:**
    - 16-bit LFSR: 0xACE1
    - 32-bit LFSR: 0xB7E15163
    - 64-bit LFSR: 0x3A7D95C2F168B4E0
    
    **Recommended Tap Positions:**
    - 16-bit LFSR: 16,15,13,4
    - 32-bit LFSR: 32,22,2,1
    - 64-bit LFSR: 64,63,61,60
    
    *These combinations create maximal-length LFSRs for better encryption.*
    """)

# Create three equal columns with fixed height for consistent image display
col1, col2, col3 = st.columns(3)

# Original Image Column
with col1:
    st.header("Original Image")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        # Create consistent container for image display
        img_container = st.container()
        with img_container:
            original_image = Image.open(uploaded_file)
            st.image(original_image, use_column_width=True)
            
            # Store original image in session state for persistence
            if "original_image_displayed" not in st.session_state:
                buf = io.BytesIO()
                original_image.save(buf, format="PNG")
                st.session_state.original_image_bytes = buf.getvalue()
                st.session_state.original_image_displayed = True
        
        # Add a processing button instead of automatic processing
        process_button = st.button("Process Image", type="primary")
        
        # Process when button is clicked or if we already have processed images
        if process_button or "encrypted_bytes" in st.session_state:
            if process_button:  # Only process if the button was actually clicked
                with st.spinner("Processing image..."):
                    try:
                        # Reset file pointer
                        uploaded_file.seek(0)
                        
                        # Prepare request data for encryption
                        data = {
                            "seed": str(int(seed)),
                            "tap_positions": tap_positions
                        }
                        
                        # Call API to encrypt image
                        response = requests.post(
                            f"{API_URL}/encrypt",
                            files={"image": uploaded_file},
                            data=data
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            encryption_id = result["encryption_id"]
                            encrypted_base64 = result["encrypted_image"]
                            
                            # Save in session state
                            st.session_state.encryption_id = encryption_id
                            st.session_state.encrypted_base64 = encrypted_base64
                            st.session_state.encrypted_bytes = base64.b64decode(encrypted_base64)
                            
                            # Immediately process decryption
                            response = requests.post(
                                f"{API_URL}/decrypt",
                                data={
                                    "encryption_id": encryption_id,
                                    "encrypted_base64": encrypted_base64
                                }
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                decrypted_base64 = result["decrypted_image"]
                                st.session_state.decrypted_bytes = base64.b64decode(decrypted_base64)
                            else:
                                st.error(f"Decryption error: {response.text}")
                        else:
                            st.error(f"Encryption error: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            # Display encrypted image with consistent styling
            with col2:
                st.header("Encrypted Image")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                if "encrypted_bytes" in st.session_state:
                    img_container = st.container()
                    with img_container:
                        encrypted_image = Image.open(io.BytesIO(st.session_state.encrypted_bytes))
                        st.image(encrypted_image, use_column_width=True)
                    
                    # Download button below the image (with key to avoid duplicates)
                    st.download_button(
                        label="Download Encrypted Image",
                        data=st.session_state.encrypted_bytes,
                        file_name="encrypted_image.png",
                        mime="image/png",
                        key="download_encrypted"
                    )
            
            # Display decrypted image with consistent styling
            with col3:
                st.header("Decrypted Image")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                if "decrypted_bytes" in st.session_state:
                    img_container = st.container()
                    with img_container:
                        decrypted_image = Image.open(io.BytesIO(st.session_state.decrypted_bytes))
                        st.image(decrypted_image, use_column_width=True)
                    
                    # Download button below the image (with key to avoid duplicates)
                    st.download_button(
                        label="Download Decrypted Image",
                        data=st.session_state.decrypted_bytes,
                        file_name="decrypted_image.png",
                        mime="image/png",
                        key="download_decrypted"
                    )

# Add a button to reprocess with new parameters if needed
if "encrypted_bytes" in st.session_state and st.sidebar.button("Reprocess with New Parameters"):
    # Clear only the encryption/decryption results but keep the original image
    for key in list(st.session_state.keys()):
        if key != "original_image_bytes" and key != "original_image_displayed":
            del st.session_state[key]
    st.rerun()