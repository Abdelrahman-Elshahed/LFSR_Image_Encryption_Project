# LFSR Image Encryption System


## Table of Contents

  - [Overview](#overview)
  - [Architecture](#architecture)
  - [Project Structure](#project-structure)
  - [Features](#features)
  - [Setup](#setup)
  - [Run with Streamlit Application](#run-with-streamlit-application)
  - [Usage](#usage)
  - [Technical Implementation](#technical-implementation)

## Overview
This project implements a web-based image encryption system using cryptographically secure Linear Feedback Shift Register (LFSR) techniques. Users can upload images, configure encryption parameters, and receive encrypted and decrypted versions in real-time.


## Architecture
The project follows a client-server architecture with:

- A core encryption/decryption module
- **Backend API** (FastAPI): Handles encryption/decryption operations
- **Frontend UI** (Streamlit): Provides user interface for image upload and parameter configuration

## Project Structure
```bash
LFSR_Image_Encryption_System/
│
├── LFSR_Encryption.py          # Core encryption & decryption logic
│
├── backend/
│   └── app.py                  # FastAPI application
│
├── frontend/
│   └── app.py                  # Streamlit application
│
├── test_images/
│   ├── lena.jpg
│   ├── test2.jpg
│   └── test5.jpg
│
├── notebook/               # Jupyter notebook
│   └── LFSR_Encryption.ipynb
│
└── README.md                   # Project documentation
   ```



## Features

- **LFSR-based encryption**: Implements confusion and diffusion principles for strong image encryption
- **Configurable parameters**: Adjustable seed values and tap positions for different security levels
- **Interactive web interface**: User-friendly Streamlit frontend
- **Real-time processing**: Immediate encryption/decryption visualization
- **Downloadable results**: Save encrypted and decrypted images

## Setup

- Clone the Repository

   ```bash
   git clone https://github.com/Abdelrahman-Elshahed/LFSR_Image_Encryption_Project.git
   ```
- Create and activate a virtual environment:
  ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
  ```
- Set up dependencies

  Install Python dependencies:
  To install all the required Python packages for the project, run the following command:
  ```bash
  pip install -r requirements.txt
  ```
## Run with Streamlit Application

   - Start the backend server:
     ```bash
     cd backend
     uvicorn app:app --reload --port 8000
     ```
  - Start the frontend (in a new terminal):
       ```bash
    cd frontend
    streamlit run app.py
     ```
   - The application will be available at [http://localhost:8501](http://localhost:8501/).

![Image](https://github.com/user-attachments/assets/49fcdd95-d549-4da3-95a6-ce6d27d26cd1)

![Image](https://github.com/user-attachments/assets/983d1d38-1665-4b8a-aa61-6d4c4169cef6)

![Image](https://github.com/user-attachments/assets/4c9eab3e-0eab-4b52-9f27-196d4b42d8d8)
## Usage

1. Upload an image using the file uploader in the left column
2. Configure encryption parameters:
- **Seed Value**: Initial state for the LFSR (hexadecimal format)
- **Tap Positions**: Comma-separated positions for LFSR feedback
3. Click "Process Image" to encrypt and decrypt
4. View the encrypted and decrypted images
5. Download results using the download buttons

- Recommended Parameters
**Seed Values**:
- 16-bit LFSR: 0xACE1
- 32-bit LFSR: 0xB7E15163
- 64-bit LFSR: 0x3A7D95C2F168B4E0

**Tap Positions**:
- 16-bit LFSR: 16,15,13,4
- 32-bit LFSR: 32,22,2,1
- 64-bit LFSR: 64,63,61,60

## Technical Implementation
### Encryption Process
1. **Confusion Layer**:

  - Generates a keystream using LFSR
  - Applies XOR operation between image pixels and keystream
2. **Diffusion Layer**:

  - Permutes pixel positions using Fisher-Yates shuffle
  - Uses LFSR values for randomization
### Decryption Process
1. **Reverse Diffusion**:

- Applies inverse permutation using stored indices
2. **Reverse Confusion**:

- Applies XOR with the same keystream (XOR is its own inverse)
