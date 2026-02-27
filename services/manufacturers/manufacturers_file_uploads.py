import os
import shutil
from pathlib import Path
from fastapi import UploadFile
from PIL import Image
import io

# Define upload directory
UPLOAD_BASE_DIR = "./uploads/manufacturers"

def create_upload_directory(manufacturer_id: int):
    # Create directory for manufacturer to store uploaded files
    upload_path = os.path.join(UPLOAD_BASE_DIR, str(manufacturer_id))
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

def save_file(file: UploadFile, upload_path: str, custom_filename: str = None) -> str:
    # Save uploaded file to specified directory with compression for images
    try:
        # Reset file pointer to beginning
        file.file.seek(0)
        
        # Extract file extension
        file_extension = file.filename.split(".")[-1].lower()
        
        # Generate filename with parameter name and extension
        if custom_filename:
            # For images, save as JPEG after compression
            if file.content_type.startswith("image/"):
                filename = f"{custom_filename}.jpg"
            else:
                # For PDFs and other files, keep original extension
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
        
        # Return a web-accessible path (served from /uploads)
        public_path = file_path.replace("\\", "/").replace("./uploads", "/uploads")
        return public_path
    except Exception as e:
        raise Exception(f"File upload failed: {str(e)}")

def delete_manufacturer_files(manufacturer_id: int):
    # Delete all files for a manufacturer
    try:
        upload_path = os.path.join(UPLOAD_BASE_DIR, str(manufacturer_id))
        if os.path.exists(upload_path):
            shutil.rmtree(upload_path)
    except Exception as e:
        raise Exception(f"File deletion failed: {str(e)}")

def validate_file(file: UploadFile, allowed_extensions: list = None) -> bool:
    # Validate if file is in allowed formats
    if allowed_extensions is None:
        allowed_extensions = ["pdf", "jpg", "jpeg", "png"]
    
    file_extension = file.filename.split(".")[-1].lower()
    return file_extension in allowed_extensions
