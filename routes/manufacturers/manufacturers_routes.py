from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Optional, List
from models.manufacturers.manufacturers_models import Manufacturer
from services.manufacturers.manufacturers_file_uploads import (
    create_upload_directory, save_file, delete_manufacturer_files, validate_file
)
from db import get_db
import json

router = APIRouter(prefix="/api/manufacturers", tags=["manufacturers"])

# Manufacturer Application POST endpoint
@router.post("/create", response_model=dict)
async def create_manufacturer(
    # Required fields
    company_name: str = Form(...),
    email: str = Form(...),
    phn_no: str = Form(...),
    bank_name: str = Form(...),
    bank_ac_no: str = Form(...),
    ifsc_code: str = Form(...),
    registered_office_address: str = Form(...),
    # Required file uploads
    incorporation_certificate: UploadFile = File(...),
    pan_url: UploadFile = File(...),
    gst_cert_url: UploadFile = File(...),
    fssai_license_url: UploadFile = File(...),
    excise_license_url: UploadFile = File(...),
    cancelled_cheque_url: UploadFile = File(...),
    auth_letter_url: UploadFile = File(...),
    manufacturer_images: List[UploadFile] = File(...),
    # Optional fields
    pan_no: Optional[str] = Form(None),
    gst_no: Optional[str] = Form(None),
    fssai_license_no: Optional[str] = Form(None),
    factory_address: Optional[str] = Form(None),
    excise_no: Optional[str] = Form(None),
    auth_signatory_name: Optional[str] = Form(None),
    alt_phn_no: Optional[str] = Form(None),
    upi_id: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Create new manufacturer record
    try:
        # Log all received parameters
        print(f"=== CREATE MANUFACTURER REQUEST ===")
        print(f"company_name: {company_name}")
        print(f"email: {email}")
        print(f"phn_no: {phn_no}")
        print(f"bank_name: {bank_name}")
        print(f"bank_ac_no: {bank_ac_no}")
        print(f"ifsc_code: {ifsc_code}")
        print(f"registered_office_address: {registered_office_address}")
        print(f"pan_no: {pan_no}")
        print(f"gst_no: {gst_no}")
        print(f"fssai_license_no: {fssai_license_no}")
        print(f"factory_address: {factory_address}")
        print(f"excise_no: {excise_no}")
        print(f"auth_signatory_name: {auth_signatory_name}")
        print(f"alt_phn_no: {alt_phn_no}")
        print(f"upi_id: {upi_id}")
        print(f"incorporation_certificate: {incorporation_certificate.filename if incorporation_certificate else None}")
        print(f"pan_url: {pan_url.filename if pan_url else None}")
        print(f"gst_cert_url: {gst_cert_url.filename if gst_cert_url else None}")
        print(f"fssai_license_url: {fssai_license_url.filename if fssai_license_url else None}")
        print(f"excise_license_url: {excise_license_url.filename if excise_license_url else None}")
        print(f"cancelled_cheque_url: {cancelled_cheque_url.filename if cancelled_cheque_url else None}")
        print(f"auth_letter_url: {auth_letter_url.filename if auth_letter_url else None}")
        print(f"manufacturer_images: {[img.filename for img in manufacturer_images] if manufacturer_images else None}")
        print(f"====================================")
        
        # Create new manufacturer instance
        new_manufacturer = Manufacturer(
            company_name=company_name,
            email=email,
            phn_no=phn_no,
            pan_no=pan_no,
            gst_no=gst_no,
            fssai_license_no=fssai_license_no,
            bank_name=bank_name,
            bank_ac_no=bank_ac_no,
            ifsc_code=ifsc_code,
            registered_office_address=registered_office_address,
            factory_address=factory_address,
            excise_no=excise_no,
            auth_signatory_name=auth_signatory_name,
            alt_phn_no=alt_phn_no,
            upi_id=upi_id,
        )
        
        # Add to database to get manufacturer_id
        db.add(new_manufacturer)
        db.flush()
        
        # Create upload directory
        upload_path = create_upload_directory(new_manufacturer.manufacturer_id)
        
        # Save required files
        if not validate_file(incorporation_certificate):
            raise HTTPException(status_code=400, detail="Invalid file format for incorporation certificate")
        new_manufacturer.incorporation_certificate_url = save_file(incorporation_certificate, upload_path, "incorporation_cert")
        
        if not validate_file(pan_url):
            raise HTTPException(status_code=400, detail="Invalid file format for PAN URL")
        new_manufacturer.pan_url = save_file(pan_url, upload_path, "pan_document")
        
        if not validate_file(gst_cert_url):
            raise HTTPException(status_code=400, detail="Invalid file format for GST certificate")
        new_manufacturer.gst_cert_url = save_file(gst_cert_url, upload_path, "gst_certificate")
        
        if not validate_file(fssai_license_url):
            raise HTTPException(status_code=400, detail="Invalid file format for FSSAI license")
        new_manufacturer.fssai_license_url = save_file(fssai_license_url, upload_path, "fssai_license")
        
        if not validate_file(excise_license_url):
            raise HTTPException(status_code=400, detail="Invalid file format for excise license")
        new_manufacturer.excise_license_url = save_file(excise_license_url, upload_path, "excise_license")
        
        if not validate_file(cancelled_cheque_url):
            raise HTTPException(status_code=400, detail="Invalid file format for cancelled cheque")
        new_manufacturer.cancelled_cheque_url = save_file(cancelled_cheque_url, upload_path, "cancelled_cheque")
        
        # Save authorization letter
        if not validate_file(auth_letter_url):
            raise HTTPException(status_code=400, detail="Invalid file format for authorization letter")
        new_manufacturer.auth_letter_url = save_file(auth_letter_url, upload_path, "auth_letter")
        
        # Save manufacturer images
        image_urls = []
        for idx, image in enumerate(manufacturer_images):
            if validate_file(image):
                image_url = save_file(image, upload_path, f"manufacturer_image_{idx}")
                image_urls.append(image_url)
        if image_urls:
            new_manufacturer.manufacturer_images_url = json.dumps(image_urls)
        else:
            raise HTTPException(status_code=400, detail="At least one valid manufacturer image is required")
        
        # Commit changes
        db.commit()
        db.refresh(new_manufacturer)
        
        return {
            "message": "Your manufacturer registration request has been submitted successfully and is pending verification. We will review your application and notify you of the status within 3-5 business days.",
            "manufacturer_id": new_manufacturer.manufacturer_id,
            "company_name": new_manufacturer.company_name
        }
    except Exception as e:
        print(f"=== ERROR IN CREATE MANUFACTURER ===")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        print(f"company_name: {company_name}")
        print(f"email: {email}")
        print(f"phn_no: {phn_no}")
        print(f"bank_name: {bank_name}")
        print(f"bank_ac_no: {bank_ac_no}")
        print(f"ifsc_code: {ifsc_code}")
        print(f"registered_office_address: {registered_office_address}")
        print(f"pan_no: {pan_no}")
        print(f"gst_no: {gst_no}")
        print(f"fssai_license_no: {fssai_license_no}")
        print(f"factory_address: {factory_address}")
        print(f"excise_no: {excise_no}")
        print(f"auth_signatory_name: {auth_signatory_name}")
        print(f"alt_phn_no: {alt_phn_no}")
        print(f"upi_id: {upi_id}")
        print(f"incorporation_certificate: {incorporation_certificate.filename if incorporation_certificate else None}")
        print(f"pan_url: {pan_url.filename if pan_url else None}")
        print(f"gst_cert_url: {gst_cert_url.filename if gst_cert_url else None}")
        print(f"fssai_license_url: {fssai_license_url.filename if fssai_license_url else None}")
        print(f"excise_license_url: {excise_license_url.filename if excise_license_url else None}")
        print(f"cancelled_cheque_url: {cancelled_cheque_url.filename if cancelled_cheque_url else None}")
        print(f"auth_letter_url: {auth_letter_url.filename if auth_letter_url else None}")
        print(f"manufacturer_images: {[img.filename for img in manufacturer_images] if manufacturer_images else None}")
        print(f"====================================")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Get all manufacturers' applications endpoint
@router.get("/get-all", response_model=list)
async def get_all_manufacturers(db: Session = Depends(get_db)):
    # Get all manufacturers
    try:
        manufacturers = db.query(Manufacturer).all()
        return manufacturers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a manufacturer's application by ID endpoint
@router.get("/get-by/{manufacturer_id}", response_model=dict)
async def get_manufacturer_by_id(manufacturer_id: int, db: Session = Depends(get_db)):
    # Get manufacturer by ID
    try:
        manufacturer = db.query(Manufacturer).filter(Manufacturer.manufacturer_id == manufacturer_id).first()
        if not manufacturer:
            raise HTTPException(status_code=404, detail="Manufacturer not found")
        return manufacturer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update a manufacturer's application by ID endpoint
@router.put("/update-by/{manufacturer_id}", response_model=dict)
async def update_manufacturer(
    manufacturer_id: int,
    # Optional text fields for update
    company_name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phn_no: Optional[str] = Form(None),
    pan_no: Optional[str] = Form(None),
    gst_no: Optional[str] = Form(None),
    fssai_license_no: Optional[str] = Form(None),
    bank_name: Optional[str] = Form(None),
    bank_ac_no: Optional[str] = Form(None),
    ifsc_code: Optional[str] = Form(None),
    registered_office_address: Optional[str] = Form(None),
    factory_address: Optional[str] = Form(None),
    excise_no: Optional[str] = Form(None),
    auth_signatory_name: Optional[str] = Form(None),
    alt_phn_no: Optional[str] = Form(None),
    upi_id: Optional[str] = Form(None),
    # Optional file uploads
    incorporation_certificate: Optional[UploadFile] = File(None),
    pan_url: Optional[UploadFile] = File(None),
    gst_cert_url: Optional[UploadFile] = File(None),
    fssai_license_url: Optional[UploadFile] = File(None),
    excise_license_url: Optional[UploadFile] = File(None),
    cancelled_cheque_url: Optional[UploadFile] = File(None),
    auth_letter_url: Optional[UploadFile] = File(None),
    manufacturer_images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    # Update manufacturer record with all fields including file uploads
    try:
        # Log update request
        print(f"=== UPDATE MANUFACTURER REQUEST (ID: {manufacturer_id}) ===")
        print(f"company_name: {company_name}")
        print(f"email: {email}")
        print(f"phn_no: {phn_no}")
        print(f"pan_no: {pan_no}")
        print(f"gst_no: {gst_no}")
        print(f"fssai_license_no: {fssai_license_no}")
        print(f"bank_name: {bank_name}")
        print(f"bank_ac_no: {bank_ac_no}")
        print(f"ifsc_code: {ifsc_code}")
        print(f"registered_office_address: {registered_office_address}")
        print(f"factory_address: {factory_address}")
        print(f"excise_no: {excise_no}")
        print(f"auth_signatory_name: {auth_signatory_name}")
        print(f"alt_phn_no: {alt_phn_no}")
        print(f"upi_id: {upi_id}")
        print(f"incorporation_certificate: {incorporation_certificate.filename if incorporation_certificate else None}")
        print(f"pan_url: {pan_url.filename if pan_url else None}")
        print(f"gst_cert_url: {gst_cert_url.filename if gst_cert_url else None}")
        print(f"fssai_license_url: {fssai_license_url.filename if fssai_license_url else None}")
        print(f"excise_license_url: {excise_license_url.filename if excise_license_url else None}")
        print(f"cancelled_cheque_url: {cancelled_cheque_url.filename if cancelled_cheque_url else None}")
        print(f"auth_letter_url: {auth_letter_url.filename if auth_letter_url else None}")
        print(f"manufacturer_images: {[img.filename for img in manufacturer_images] if manufacturer_images else None}")
        print(f"====================================")
        
        # Retrieve manufacturer record
        manufacturer = db.query(Manufacturer).filter(Manufacturer.manufacturer_id == manufacturer_id).first()
        if not manufacturer:
            raise HTTPException(status_code=404, detail="Manufacturer not found")
        
        # Update text fields
        if company_name:
            manufacturer.company_name = company_name
        if email:
            manufacturer.email = email
        if phn_no:
            manufacturer.phn_no = phn_no
        if pan_no:
            manufacturer.pan_no = pan_no
        if gst_no:
            manufacturer.gst_no = gst_no
        if fssai_license_no:
            manufacturer.fssai_license_no = fssai_license_no
        if bank_name:
            manufacturer.bank_name = bank_name
        if bank_ac_no:
            manufacturer.bank_ac_no = bank_ac_no
        if ifsc_code:
            manufacturer.ifsc_code = ifsc_code
        if registered_office_address:
            manufacturer.registered_office_address = registered_office_address
        if factory_address:
            manufacturer.factory_address = factory_address
        if excise_no:
            manufacturer.excise_no = excise_no
        if auth_signatory_name:
            manufacturer.auth_signatory_name = auth_signatory_name
        if alt_phn_no:
            manufacturer.alt_phn_no = alt_phn_no
        if upi_id:
            manufacturer.upi_id = upi_id
        
        # Create upload directory path
        upload_path = f"./uploads/manufacturers/{manufacturer_id}"
        
        # Update file uploads and replace old files
        if incorporation_certificate and validate_file(incorporation_certificate):
            manufacturer.incorporation_certificate_url = save_file(incorporation_certificate, upload_path, "incorporation_cert")
        
        if pan_url and validate_file(pan_url):
            manufacturer.pan_url = save_file(pan_url, upload_path, "pan_document")
        
        if gst_cert_url and validate_file(gst_cert_url):
            manufacturer.gst_cert_url = save_file(gst_cert_url, upload_path, "gst_certificate")
        
        if fssai_license_url and validate_file(fssai_license_url):
            manufacturer.fssai_license_url = save_file(fssai_license_url, upload_path, "fssai_license")
        
        if excise_license_url and validate_file(excise_license_url):
            manufacturer.excise_license_url = save_file(excise_license_url, upload_path, "excise_license")
        
        if cancelled_cheque_url and validate_file(cancelled_cheque_url):
            manufacturer.cancelled_cheque_url = save_file(cancelled_cheque_url, upload_path, "cancelled_cheque")
        
        if auth_letter_url and validate_file(auth_letter_url):
            manufacturer.auth_letter_url = save_file(auth_letter_url, upload_path, "auth_letter")
        
        # Update manufacturer images
        if manufacturer_images:
            image_urls = []
            for idx, image in enumerate(manufacturer_images):
                if validate_file(image):
                    image_url = save_file(image, upload_path, f"manufacturer_image_{idx}")
                    image_urls.append(image_url)
            if image_urls:
                manufacturer.manufacturer_images_url = json.dumps(image_urls)
        
        # Commit changes
        db.commit()
        db.refresh(manufacturer)
        
        return {
            "message": "Manufacturer updated successfully",
            "manufacturer_id": manufacturer.manufacturer_id,
            "company_name": manufacturer.company_name
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"=== ERROR IN UPDATE MANUFACTURER ===")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        print(f"====================================")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Delete a manufacturer's application by ID endpoint
@router.delete("/delete-by/{manufacturer_id}", response_model=dict)
async def delete_manufacturer(manufacturer_id: int, db: Session = Depends(get_db)):
    # Delete manufacturer and associated files
    try:
        manufacturer = db.query(Manufacturer).filter(Manufacturer.manufacturer_id == manufacturer_id).first()
        if not manufacturer:
            raise HTTPException(status_code=404, detail="Manufacturer not found")
        
        # Delete files
        delete_manufacturer_files(manufacturer_id)
        
        # Delete database record
        db.delete(manufacturer)
        db.commit()
        
        return {"message": "Manufacturer deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
