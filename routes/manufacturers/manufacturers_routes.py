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
    trade_license_url: UploadFile = File(...),
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
        print(f"\n{'='*60}")
        print(f"=== CREATE MANUFACTURER REQUEST ===")
        print(f"{'='*60}")
        print(f"[INFO] Request started for creating new manufacturer")
        print(f"[PARAM] company_name: {company_name}")
        print(f"[PARAM] email: {email}")
        print(f"[PARAM] phn_no: {phn_no}")
        print(f"[PARAM] bank_name: {bank_name}")
        print(f"[PARAM] bank_ac_no: {bank_ac_no}")
        print(f"[PARAM] ifsc_code: {ifsc_code}")
        print(f"[PARAM] registered_office_address: {registered_office_address}")
        print(f"[PARAM] pan_no: {pan_no}")
        print(f"[PARAM] gst_no: {gst_no}")
        print(f"[PARAM] fssai_license_no: {fssai_license_no}")
        print(f"[PARAM] factory_address: {factory_address}")
        print(f"[PARAM] excise_no: {excise_no}")
        print(f"[PARAM] auth_signatory_name: {auth_signatory_name}")
        print(f"[PARAM] alt_phn_no: {alt_phn_no}")
        print(f"[PARAM] upi_id: {upi_id}")
        print(f"[FILE] incorporation_certificate: {incorporation_certificate.filename if incorporation_certificate else None}")
        print(f"[FILE] pan_url: {pan_url.filename if pan_url else None}")
        print(f"[FILE] gst_cert_url: {gst_cert_url.filename if gst_cert_url else None}")
        print(f"[FILE] fssai_license_url: {fssai_license_url.filename if fssai_license_url else None}")
        print(f"[FILE] trade_license_url: {trade_license_url.filename if trade_license_url else None}")
        print(f"[FILE] excise_license_url: {excise_license_url.filename if excise_license_url else None}")
        print(f"[FILE] cancelled_cheque_url: {cancelled_cheque_url.filename if cancelled_cheque_url else None}")
        print(f"[FILE] auth_letter_url: {auth_letter_url.filename if auth_letter_url else None}")
        print(f"[FILE] manufacturer_images: {[img.filename for img in manufacturer_images] if manufacturer_images else None}")
        
        # Create new manufacturer instance
        print(f"\n[STEP] Creating new manufacturer instance")
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
            # Initialize required file URL fields to avoid NOT NULL constraint failures
            incorporation_certificate_url="",
            pan_url="",
            gst_cert_url="",
            fssai_license_url="",
            trade_license_url="",
            excise_license_url="",
            cancelled_cheque_url="",
            auth_letter_url="",
            manufacturer_images_url=[],
        )
        print(f"[SUCCESS] Manufacturer instance created")
        
        # Add to database to get manufacturer_id
        print(f"[STEP] Adding manufacturer to database")
        db.add(new_manufacturer)
        db.flush()
        print(f"[SUCCESS] Manufacturer added to database with ID: {new_manufacturer.manufacturer_id}")
        
        # Create upload directory
        print(f"[STEP] Creating upload directory for manufacturer_id: {new_manufacturer.manufacturer_id}")
        upload_path = create_upload_directory(new_manufacturer.manufacturer_id)
        print(f"[SUCCESS] Upload directory created at: {upload_path}")
        
        # Save required files
        print(f"\n[STEP] Starting file uploads processing")
        
        if not validate_file(incorporation_certificate):
            raise HTTPException(status_code=400, detail="Invalid file format for incorporation certificate")
        print(f"[PROCESS] Uploading incorporation_certificate: {incorporation_certificate.filename}")
        new_manufacturer.incorporation_certificate_url = save_file(incorporation_certificate, upload_path, "incorporation_cert")
        print(f"[SUCCESS] incorporation_certificate saved at: {new_manufacturer.incorporation_certificate_url}")
        
        if not validate_file(pan_url):
            raise HTTPException(status_code=400, detail="Invalid file format for PAN URL")
        print(f"[PROCESS] Uploading pan_url: {pan_url.filename}")
        new_manufacturer.pan_url = save_file(pan_url, upload_path, "pan_document")
        print(f"[SUCCESS] pan_url saved at: {new_manufacturer.pan_url}")
        
        if not validate_file(gst_cert_url):
            raise HTTPException(status_code=400, detail="Invalid file format for GST certificate")
        print(f"[PROCESS] Uploading gst_cert_url: {gst_cert_url.filename}")
        new_manufacturer.gst_cert_url = save_file(gst_cert_url, upload_path, "gst_certificate")
        print(f"[SUCCESS] gst_cert_url saved at: {new_manufacturer.gst_cert_url}")
        
        if not validate_file(fssai_license_url):
            raise HTTPException(status_code=400, detail="Invalid file format for FSSAI license")
        print(f"[PROCESS] Uploading fssai_license_url: {fssai_license_url.filename}")
        new_manufacturer.fssai_license_url = save_file(fssai_license_url, upload_path, "fssai_license")
        print(f"[SUCCESS] fssai_license_url saved at: {new_manufacturer.fssai_license_url}")
        
        if not validate_file(trade_license_url):
            raise HTTPException(status_code=400, detail="Invalid file format for trade license")
        print(f"[PROCESS] Uploading trade_license_url: {trade_license_url.filename}")
        new_manufacturer.trade_license_url = save_file(trade_license_url, upload_path, "trade_license")
        print(f"[SUCCESS] trade_license_url saved at: {new_manufacturer.trade_license_url}")
        
        if not validate_file(excise_license_url):
            raise HTTPException(status_code=400, detail="Invalid file format for excise license")
        print(f"[PROCESS] Uploading excise_license_url: {excise_license_url.filename}")
        new_manufacturer.excise_license_url = save_file(excise_license_url, upload_path, "excise_license")
        print(f"[SUCCESS] excise_license_url saved at: {new_manufacturer.excise_license_url}")
        
        if not validate_file(cancelled_cheque_url):
            raise HTTPException(status_code=400, detail="Invalid file format for cancelled cheque")
        print(f"[PROCESS] Uploading cancelled_cheque_url: {cancelled_cheque_url.filename}")
        new_manufacturer.cancelled_cheque_url = save_file(cancelled_cheque_url, upload_path, "cancelled_cheque")
        print(f"[SUCCESS] cancelled_cheque_url saved at: {new_manufacturer.cancelled_cheque_url}")
        
        # Save authorization letter
        if not validate_file(auth_letter_url):
            raise HTTPException(status_code=400, detail="Invalid file format for authorization letter")
        print(f"[PROCESS] Uploading auth_letter_url: {auth_letter_url.filename}")
        new_manufacturer.auth_letter_url = save_file(auth_letter_url, upload_path, "auth_letter")
        print(f"[SUCCESS] auth_letter_url saved at: {new_manufacturer.auth_letter_url}")
        
        # Save manufacturer images
        print(f"[PROCESS] Uploading manufacturer_images: {len(manufacturer_images)} image(s)")
        image_urls = []
        for idx, image in enumerate(manufacturer_images):
            if validate_file(image):
                print(f"[PROCESS] Processing image {idx + 1}: {image.filename}")
                image_url = save_file(image, upload_path, f"manufacturer_image_{idx}")
                image_urls.append(image_url)
                print(f"[SUCCESS] Image {idx + 1} saved at: {image_url}")
        if image_urls:
            new_manufacturer.manufacturer_images_url = json.dumps(image_urls)
            print(f"[SUCCESS] All {len(image_urls)} manufacturer images processed and saved")
        else:
            raise HTTPException(status_code=400, detail="At least one valid manufacturer image is required")
        
        # Commit changes
        print(f"\n[STEP] Committing changes to database")
        db.commit()
        print(f"[SUCCESS] Database transaction committed")
        
        # Refresh to get latest data
        print(f"[STEP] Refreshing manufacturer record from database")
        db.refresh(new_manufacturer)
        print(f"[SUCCESS] Manufacturer record refreshed")
        
        print(f"\n[FINAL] Manufacturer registration completed successfully!")
        print(f"[RESULT] Manufacturer ID: {new_manufacturer.manufacturer_id}")
        print(f"[RESULT] Company Name: {new_manufacturer.company_name}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Your manufacturer registration request has been submitted successfully and is pending verification. We will review your application and notify you of the status within 3-5 business days.",
            "manufacturer_id": new_manufacturer.manufacturer_id,
            "company_name": new_manufacturer.company_name,
            "api_logs": [
                "[INFO] Request started for creating new manufacturer",
                f"[PARAM] company_name: {company_name}",
                f"[PARAM] email: {email}",
                f"[PARAM] phn_no: {phn_no}",
                f"[PARAM] bank_name: {bank_name}",
                f"[PARAM] bank_ac_no: {bank_ac_no}",
                f"[PARAM] ifsc_code: {ifsc_code}",
                f"[PARAM] registered_office_address: {registered_office_address}",
                f"[FILE] incorporation_certificate: {incorporation_certificate.filename if incorporation_certificate else None}",
                f"[FILE] pan_url: {pan_url.filename if pan_url else None}",
                f"[FILE] gst_cert_url: {gst_cert_url.filename if gst_cert_url else None}",
                f"[FILE] fssai_license_url: {fssai_license_url.filename if fssai_license_url else None}",
                f"[FILE] excise_license_url: {excise_license_url.filename if excise_license_url else None}",
                f"[FILE] cancelled_cheque_url: {cancelled_cheque_url.filename if cancelled_cheque_url else None}",
                f"[FILE] auth_letter_url: {auth_letter_url.filename if auth_letter_url else None}",
                f"[STEP] Creating new manufacturer instance",
                "[SUCCESS] Manufacturer instance created",
                "[STEP] Adding manufacturer to database",
                f"[SUCCESS] Manufacturer added to database with ID: {new_manufacturer.manufacturer_id}",
                f"[STEP] Creating upload directory for manufacturer_id: {new_manufacturer.manufacturer_id}",
                "[SUCCESS] Upload directory created",
                "[STEP] Starting file uploads processing",
                f"[SUCCESS] All required documents processed and saved",
                f"[SUCCESS] All {len(json.loads(new_manufacturer.manufacturer_images_url))} manufacturer images processed and saved",
                "[STEP] Committing changes to database",
                "[SUCCESS] Database transaction committed",
                "[SUCCESS] Manufacturer record refreshed",
                "[FINAL] Manufacturer registration completed successfully!"
            ]
        }
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"=== ERROR IN CREATE MANUFACTURER ===")
        print(f"{'='*60}")
        print(f"[ERROR] Error Type: {type(e).__name__}")
        print(f"[ERROR] Error Message: {str(e)}")
        print(f"[ERROR-PARAM] company_name: {company_name}")
        print(f"[ERROR-PARAM] email: {email}")
        print(f"[ERROR-PARAM] phn_no: {phn_no}")
        print(f"[ERROR-PARAM] bank_name: {bank_name}")
        print(f"[ERROR-PARAM] bank_ac_no: {bank_ac_no}")
        print(f"[ERROR-PARAM] ifsc_code: {ifsc_code}")
        print(f"[ERROR-PARAM] registered_office_address: {registered_office_address}")
        print(f"[ERROR-PARAM] pan_no: {pan_no}")
        print(f"[ERROR-PARAM] gst_no: {gst_no}")
        print(f"[ERROR-PARAM] fssai_license_no: {fssai_license_no}")
        print(f"[ERROR-PARAM] factory_address: {factory_address}")
        print(f"[ERROR-PARAM] excise_no: {excise_no}")
        print(f"[ERROR-PARAM] auth_signatory_name: {auth_signatory_name}")
        print(f"[ERROR-PARAM] alt_phn_no: {alt_phn_no}")
        print(f"[ERROR-PARAM] upi_id: {upi_id}")
        print(f"[ERROR-FILE] incorporation_certificate: {incorporation_certificate.filename if incorporation_certificate else None}")
        print(f"[ERROR-FILE] pan_url: {pan_url.filename if pan_url else None}")
        print(f"[ERROR-FILE] gst_cert_url: {gst_cert_url.filename if gst_cert_url else None}")
        print(f"[ERROR-FILE] fssai_license_url: {fssai_license_url.filename if fssai_license_url else None}")
        print(f"[ERROR-FILE] excise_license_url: {excise_license_url.filename if excise_license_url else None}")
        print(f"[ERROR-FILE] cancelled_cheque_url: {cancelled_cheque_url.filename if cancelled_cheque_url else None}")
        print(f"[ERROR-FILE] auth_letter_url: {auth_letter_url.filename if auth_letter_url else None}")
        print(f"[ERROR-FILE] manufacturer_images: {[img.filename for img in manufacturer_images] if manufacturer_images else None}")
        print(f"{'='*60}\n")
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
    trade_license_url: Optional[UploadFile] = File(None),
    excise_license_url: Optional[UploadFile] = File(None),
    cancelled_cheque_url: Optional[UploadFile] = File(None),
    auth_letter_url: Optional[UploadFile] = File(None),
    manufacturer_images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    # Update manufacturer record with all fields including file uploads
    try:
        # Log update request
        print(f"\n{'='*60}")
        print(f"=== UPDATE MANUFACTURER REQUEST (ID: {manufacturer_id}) ===")
        print(f"{'='*60}")
        print(f"[INFO] Request started for updating manufacturer_id: {manufacturer_id}")
        print(f"[PARAM] company_name: {company_name}")
        print(f"[PARAM] email: {email}")
        print(f"[PARAM] phn_no: {phn_no}")
        print(f"[PARAM] pan_no: {pan_no}")
        print(f"[PARAM] gst_no: {gst_no}")
        print(f"[PARAM] fssai_license_no: {fssai_license_no}")
        print(f"[PARAM] bank_name: {bank_name}")
        print(f"[PARAM] bank_ac_no: {bank_ac_no}")
        print(f"[PARAM] ifsc_code: {ifsc_code}")
        print(f"[PARAM] registered_office_address: {registered_office_address}")
        print(f"[PARAM] factory_address: {factory_address}")
        print(f"[PARAM] excise_no: {excise_no}")
        print(f"[PARAM] auth_signatory_name: {auth_signatory_name}")
        print(f"[PARAM] alt_phn_no: {alt_phn_no}")
        print(f"[PARAM] upi_id: {upi_id}")
        print(f"[FILE] incorporation_certificate: {incorporation_certificate.filename if incorporation_certificate else None}")
        print(f"[FILE] pan_url: {pan_url.filename if pan_url else None}")
        print(f"[FILE] gst_cert_url: {gst_cert_url.filename if gst_cert_url else None}")
        print(f"[FILE] fssai_license_url: {fssai_license_url.filename if fssai_license_url else None}")
        print(f"[FILE] excise_license_url: {excise_license_url.filename if excise_license_url else None}")
        print(f"[FILE] cancelled_cheque_url: {cancelled_cheque_url.filename if cancelled_cheque_url else None}")
        print(f"[FILE] auth_letter_url: {auth_letter_url.filename if auth_letter_url else None}")
        print(f"[FILE] manufacturer_images: {[img.filename for img in manufacturer_images] if manufacturer_images else None}")
        
        # Retrieve manufacturer record
        print(f"\n[STEP] Fetching manufacturer record from database")
        manufacturer = db.query(Manufacturer).filter(Manufacturer.manufacturer_id == manufacturer_id).first()
        if not manufacturer:
            print(f"[ERROR] Manufacturer with ID {manufacturer_id} not found")
            raise HTTPException(status_code=404, detail="Manufacturer not found")
        print(f"[SUCCESS] Manufacturer record found")
        
        # Update text fields
        print(f"\n[STEP] Updating text fields")
        if company_name:
            print(f"[UPDATE] company_name: {company_name}")
            manufacturer.company_name = company_name
        if email:
            print(f"[UPDATE] email: {email}")
            manufacturer.email = email
        if phn_no:
            print(f"[UPDATE] phn_no: {phn_no}")
            manufacturer.phn_no = phn_no
        if pan_no:
            print(f"[UPDATE] pan_no: {pan_no}")
            manufacturer.pan_no = pan_no
        if gst_no:
            print(f"[UPDATE] gst_no: {gst_no}")
            manufacturer.gst_no = gst_no
        if fssai_license_no:
            print(f"[UPDATE] fssai_license_no: {fssai_license_no}")
            manufacturer.fssai_license_no = fssai_license_no
        if bank_name:
            print(f"[UPDATE] bank_name: {bank_name}")
            manufacturer.bank_name = bank_name
        if bank_ac_no:
            print(f"[UPDATE] bank_ac_no: {bank_ac_no}")
            manufacturer.bank_ac_no = bank_ac_no
        if ifsc_code:
            print(f"[UPDATE] ifsc_code: {ifsc_code}")
            manufacturer.ifsc_code = ifsc_code
        if registered_office_address:
            print(f"[UPDATE] registered_office_address: {registered_office_address}")
            manufacturer.registered_office_address = registered_office_address
        if factory_address:
            print(f"[UPDATE] factory_address: {factory_address}")
            manufacturer.factory_address = factory_address
        if excise_no:
            print(f"[UPDATE] excise_no: {excise_no}")
            manufacturer.excise_no = excise_no
        if auth_signatory_name:
            print(f"[UPDATE] auth_signatory_name: {auth_signatory_name}")
            manufacturer.auth_signatory_name = auth_signatory_name
        if alt_phn_no:
            print(f"[UPDATE] alt_phn_no: {alt_phn_no}")
            manufacturer.alt_phn_no = alt_phn_no
        if upi_id:
            print(f"[UPDATE] upi_id: {upi_id}")
            manufacturer.upi_id = upi_id
        print(f"[SUCCESS] All text fields updated")
        
        # Create upload directory path
        upload_path = f"./uploads/manufacturers/{manufacturer_id}"
        
        # Update file uploads and replace old files
        print(f"\n[STEP] Starting file uploads update processing")
        
        if incorporation_certificate and validate_file(incorporation_certificate):
            print(f"[PROCESS] Updating incorporation_certificate: {incorporation_certificate.filename}")
            old_url = manufacturer.incorporation_certificate_url
            manufacturer.incorporation_certificate_url = save_file(incorporation_certificate, upload_path, "incorporation_cert")
            print(f"[SUCCESS] incorporation_certificate replaced - Old: {old_url} -> New: {manufacturer.incorporation_certificate_url}")
        
        if pan_url and validate_file(pan_url):
            print(f"[PROCESS] Updating pan_url: {pan_url.filename}")
            old_url = manufacturer.pan_url
            manufacturer.pan_url = save_file(pan_url, upload_path, "pan_document")
            print(f"[SUCCESS] pan_url replaced - Old: {old_url} -> New: {manufacturer.pan_url}")
        
        if gst_cert_url and validate_file(gst_cert_url):
            print(f"[PROCESS] Updating gst_cert_url: {gst_cert_url.filename}")
            old_url = manufacturer.gst_cert_url
            manufacturer.gst_cert_url = save_file(gst_cert_url, upload_path, "gst_certificate")
            print(f"[SUCCESS] gst_cert_url replaced - Old: {old_url} -> New: {manufacturer.gst_cert_url}")
        
        if fssai_license_url and validate_file(fssai_license_url):
            print(f"[PROCESS] Updating fssai_license_url: {fssai_license_url.filename}")
            old_url = manufacturer.fssai_license_url
            manufacturer.fssai_license_url = save_file(fssai_license_url, upload_path, "fssai_license")
            print(f"[SUCCESS] fssai_license_url replaced - Old: {old_url} -> New: {manufacturer.fssai_license_url}")
        
        if trade_license_url and validate_file(trade_license_url):
            print(f"[PROCESS] Updating trade_license_url: {trade_license_url.filename}")
            old_url = manufacturer.trade_license_url
            manufacturer.trade_license_url = save_file(trade_license_url, upload_path, "trade_license")
            print(f"[SUCCESS] trade_license_url replaced - Old: {old_url} -> New: {manufacturer.trade_license_url}")
        
        if excise_license_url and validate_file(excise_license_url):
            print(f"[PROCESS] Updating excise_license_url: {excise_license_url.filename}")
            old_url = manufacturer.excise_license_url
            manufacturer.excise_license_url = save_file(excise_license_url, upload_path, "excise_license")
            print(f"[SUCCESS] excise_license_url replaced - Old: {old_url} -> New: {manufacturer.excise_license_url}")
        
        if cancelled_cheque_url and validate_file(cancelled_cheque_url):
            print(f"[PROCESS] Updating cancelled_cheque_url: {cancelled_cheque_url.filename}")
            old_url = manufacturer.cancelled_cheque_url
            manufacturer.cancelled_cheque_url = save_file(cancelled_cheque_url, upload_path, "cancelled_cheque")
            print(f"[SUCCESS] cancelled_cheque_url replaced - Old: {old_url} -> New: {manufacturer.cancelled_cheque_url}")
        
        if auth_letter_url and validate_file(auth_letter_url):
            print(f"[PROCESS] Updating auth_letter_url: {auth_letter_url.filename}")
            old_url = manufacturer.auth_letter_url
            manufacturer.auth_letter_url = save_file(auth_letter_url, upload_path, "auth_letter")
            print(f"[SUCCESS] auth_letter_url replaced - Old: {old_url} -> New: {manufacturer.auth_letter_url}")
        
        # Update manufacturer images
        if manufacturer_images:
            print(f"[PROCESS] Updating manufacturer_images: {len(manufacturer_images)} image(s)")
            image_urls = []
            for idx, image in enumerate(manufacturer_images):
                if validate_file(image):
                    print(f"[PROCESS] Processing image {idx + 1}: {image.filename}")
                    image_url = save_file(image, upload_path, f"manufacturer_image_{idx}")
                    image_urls.append(image_url)
                    print(f"[SUCCESS] Image {idx + 1} updated at: {image_url}")
            if image_urls:
                old_images = manufacturer.manufacturer_images_url
                manufacturer.manufacturer_images_url = json.dumps(image_urls)
                print(f"[SUCCESS] All {len(image_urls)} manufacturer images updated - Old: {old_images} -> New: {manufacturer.manufacturer_images_url}")
        
        # Commit changes
        print(f"\n[STEP] Committing changes to database")
        db.commit()
        print(f"[SUCCESS] Database transaction committed")
        
        # Refresh to get latest data
        print(f"[STEP] Refreshing manufacturer record from database")
        db.refresh(manufacturer)
        print(f"[SUCCESS] Manufacturer record refreshed")
        
        print(f"\n[FINAL] Manufacturer update completed successfully!")
        print(f"[RESULT] Manufacturer ID: {manufacturer.manufacturer_id}")
        print(f"[RESULT] Company Name: {manufacturer.company_name}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Manufacturer updated successfully",
            "manufacturer_id": manufacturer.manufacturer_id,
            "company_name": manufacturer.company_name,
            "api_logs": [
                f"[INFO] Update request started for manufacturer_id: {manufacturer_id}",
                "[STEP] Fetching manufacturer record from database",
                "[SUCCESS] Manufacturer record found",
                "[STEP] Updating text fields",
                "[SUCCESS] All text fields updated (if provided)",
                "[STEP] Starting file uploads update processing",
                "[SUCCESS] All file uploads processed (if provided)",
                "[STEP] Committing changes to database",
                "[SUCCESS] Database transaction committed",
                "[SUCCESS] Manufacturer record refreshed",
                "[FINAL] Manufacturer update completed successfully!"
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"=== ERROR IN UPDATE MANUFACTURER (ID: {manufacturer_id}) ===")
        print(f"{'='*60}")
        print(f"[ERROR] Error Type: {type(e).__name__}")
        print(f"[ERROR] Error Message: {str(e)}")
        print(f"[ERROR-PARAM] company_name: {company_name}")
        print(f"[ERROR-PARAM] email: {email}")
        print(f"[ERROR-PARAM] phn_no: {phn_no}")
        print(f"[ERROR-PARAM] pan_no: {pan_no}")
        print(f"[ERROR-PARAM] gst_no: {gst_no}")
        print(f"[ERROR-PARAM] fssai_license_no: {fssai_license_no}")
        print(f"[ERROR-PARAM] bank_name: {bank_name}")
        print(f"[ERROR-PARAM] bank_ac_no: {bank_ac_no}")
        print(f"[ERROR-PARAM] ifsc_code: {ifsc_code}")
        print(f"[ERROR-PARAM] registered_office_address: {registered_office_address}")
        print(f"[ERROR-PARAM] factory_address: {factory_address}")
        print(f"[ERROR-PARAM] excise_no: {excise_no}")
        print(f"[ERROR-PARAM] auth_signatory_name: {auth_signatory_name}")
        print(f"[ERROR-PARAM] alt_phn_no: {alt_phn_no}")
        print(f"[ERROR-PARAM] upi_id: {upi_id}")
        print(f"[ERROR-FILE] incorporation_certificate: {incorporation_certificate.filename if incorporation_certificate else None}")
        print(f"[ERROR-FILE] pan_url: {pan_url.filename if pan_url else None}")
        print(f"[ERROR-FILE] gst_cert_url: {gst_cert_url.filename if gst_cert_url else None}")
        print(f"[ERROR-FILE] fssai_license_url: {fssai_license_url.filename if fssai_license_url else None}")
        print(f"[ERROR-FILE] excise_license_url: {excise_license_url.filename if excise_license_url else None}")
        print(f"[ERROR-FILE] cancelled_cheque_url: {cancelled_cheque_url.filename if cancelled_cheque_url else None}")
        print(f"[ERROR-FILE] auth_letter_url: {auth_letter_url.filename if auth_letter_url else None}")
        print(f"[ERROR-FILE] manufacturer_images: {[img.filename for img in manufacturer_images] if manufacturer_images else None}")
        print(f"{'='*60}\n")
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
