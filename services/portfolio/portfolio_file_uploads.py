import os
import shutil
from pathlib import Path
from fastapi import UploadFile
from PIL import Image
import io

# Define upload directory
UPLOAD_BASE_DIR = "./uploads/portfolio"

def create_upload_directory():
    # Create directory for portfolio to store uploaded files
    upload_path = UPLOAD_BASE_DIR
    Path(upload_path).mkdir(parents=True, exist_ok=True)
    return upload_path

def compress_image(file: UploadFile, quality: int = 85) -> bytes:
    # Compress image file and return as bytes
    try:
        # Reset file pointer to beginning
        file.file.seek(0)
        image = Image.open(file.file)
        # Convert RGBA to RGB if necessary
        if image.mode == "RGBA":
            image = image.convert("RGB")
        # Compress image
        output = io.BytesIO()
        image.save(output, format="JPEG", quality=quality, optimize=True)
        return output.getvalue()
    except Exception as e:
        raise Exception(f"Image compression failed: {str(e)}")

def save_file(file: UploadFile, custom_filename: str = None) -> str:
    # Save uploaded file to portfolio upload directory with compression for images
    try:
        # Reset file pointer to beginning
        file.file.seek(0)
        
        # Extract file extension
        file_extension = file.filename.split(".")[-1].lower()
        
        # Create upload directory
        upload_path = create_upload_directory()
        
        # Generate filename with parameter name and extension
        if custom_filename:
            # For images, save as JPEG after compression
            if file.content_type.startswith("image/"):
                filename = f"{custom_filename}.jpg"
            else:
                # For other files, keep original extension
                filename = f"{custom_filename}.{file_extension}"
        else:
            filename = file.filename
        
        file_path = os.path.join(upload_path, filename)
        
        # Read file content
        content = file.file.read()
        
        # Compress if it's an image
        if file.content_type.startswith("image/"):
            content = compress_image(file)
        
        # Write file to disk
        with open(file_path, "wb") as f:
            f.write(content)
        
        return f"{upload_path}/{filename}"
    except Exception as e:
        raise Exception(f"File upload failed: {str(e)}")

def validate_file(file: UploadFile, allowed_extensions: list = None) -> bool:
    # Validate if file is in allowed formats
    if allowed_extensions is None:
        allowed_extensions = ["png", "jpg", "jpeg", "webp", "gif"]
    
    if not file:
        return False
    
    file_extension = file.filename.split(".")[-1].lower()
    return file_extension in allowed_extensions
