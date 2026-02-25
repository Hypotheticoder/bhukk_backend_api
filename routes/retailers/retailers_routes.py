from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Optional, List
from models.retailers.retailers_models import Retailer
from services.retailers.retailers_file_uploads import (
    create_upload_directory, save_file, delete_retailer_files, validate_file
)
from db import get_db
import json

router = APIRouter(prefix="/api/retailers", tags=["retailers"])

# Retailer Application POST endpoint
@router.post("/create", response_model=dict)
async def create_retailer(
    # Required fields
    shop_name: str = Form(...),
    license_issuing_authority: str = Form(...),
    license_valid_from: str = Form(...),
    license_valid_upto: str = Form(...),
    registered_address: str = Form(...),
    phn_no: str = Form(...),
    email: str = Form(...),
    bank_name: str = Form(...),
    bank_ac_no: str = Form(...),
    ifsc_code: str = Form(...),
    # Required file uploads
    cancelled_cheque_url: UploadFile = File(...),
    excise_license_url: UploadFile = File(...),
    trade_license_url: UploadFile = File(...),
    shop_establishment_license_url: UploadFile = File(...),
    gst_certificate_url: UploadFile = File(...),
    fire_noc_url: UploadFile = File(...),
    # Optional fields
    license_type: Optional[str] = Form(None),
    excise_license_no: Optional[str] = Form(None),
    gst_no: Optional[str] = Form(None),
    pan_no: Optional[str] = Form(None),
    owner_name: Optional[str] = Form(None),
    ownership_type: Optional[str] = Form(None),
    shop_photo_url_file: Optional[UploadFile] = File(None),
    opening_time: Optional[str] = Form(None),
    closing_time: Optional[str] = Form(None),
    bank_branch_name: Optional[str] = Form(None),
    upi_id: Optional[str] = Form(None),
    alt_phn: Optional[str] = Form(None),
    authorized_signatory_name: Optional[str] = Form(None),
    remarks: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Create new retailer record
    try:
        # Initialize messages list for response
        api_messages = []
        
        # Log all received parameters
        print(f"\n{'='*60}")
        print(f"=== CREATE RETAILER REQUEST ===")
        print(f"{'='*60}")
        api_messages.append("=== CREATE RETAILER REQUEST ===")
        
        print(f"[INFO] Request started for creating new retailer")
        api_messages.append("[INFO] Request started for creating new retailer")
        
        print(f"[PARAM] shop_name: {shop_name}")
        api_messages.append(f"[PARAM] shop_name: {shop_name}")
        print(f"[PARAM] license_issuing_authority: {license_issuing_authority}")
        api_messages.append(f"[PARAM] license_issuing_authority: {license_issuing_authority}")
        print(f"[PARAM] license_valid_from: {license_valid_from}")
        api_messages.append(f"[PARAM] license_valid_from: {license_valid_from}")
        print(f"[PARAM] license_valid_upto: {license_valid_upto}")
        api_messages.append(f"[PARAM] license_valid_upto: {license_valid_upto}")
        print(f"[PARAM] registered_address: {registered_address}")
        api_messages.append(f"[PARAM] registered_address: {registered_address}")
        print(f"[PARAM] phn_no: {phn_no}")
        api_messages.append(f"[PARAM] phn_no: {phn_no}")
        print(f"[PARAM] email: {email}")
        api_messages.append(f"[PARAM] email: {email}")
        print(f"[PARAM] bank_name: {bank_name}")
        api_messages.append(f"[PARAM] bank_name: {bank_name}")
        print(f"[PARAM] bank_ac_no: {bank_ac_no}")
        api_messages.append(f"[PARAM] bank_ac_no: {bank_ac_no}")
        print(f"[PARAM] ifsc_code: {ifsc_code}")
        api_messages.append(f"[PARAM] ifsc_code: {ifsc_code}")
        print(f"[PARAM] license_type: {license_type}")
        api_messages.append(f"[PARAM] license_type: {license_type}")
        print(f"[PARAM] excise_license_no: {excise_license_no}")
        api_messages.append(f"[PARAM] excise_license_no: {excise_license_no}")
        print(f"[PARAM] gst_no: {gst_no}")
        api_messages.append(f"[PARAM] gst_no: {gst_no}")
        print(f"[PARAM] pan_no: {pan_no}")
        api_messages.append(f"[PARAM] pan_no: {pan_no}")
        print(f"[PARAM] owner_name: {owner_name}")
        api_messages.append(f"[PARAM] owner_name: {owner_name}")
        print(f"[PARAM] ownership_type: {ownership_type}")
        api_messages.append(f"[PARAM] ownership_type: {ownership_type}")
        print(f"[PARAM] opening_time: {opening_time}")
        api_messages.append(f"[PARAM] opening_time: {opening_time}")
        print(f"[PARAM] closing_time: {closing_time}")
        api_messages.append(f"[PARAM] closing_time: {closing_time}")
        print(f"[PARAM] bank_branch_name: {bank_branch_name}")
        api_messages.append(f"[PARAM] bank_branch_name: {bank_branch_name}")
        print(f"[PARAM] upi_id: {upi_id}")
        api_messages.append(f"[PARAM] upi_id: {upi_id}")
        print(f"[PARAM] alt_phn: {alt_phn}")
        api_messages.append(f"[PARAM] alt_phn: {alt_phn}")
        print(f"[PARAM] authorized_signatory_name: {authorized_signatory_name}")
        api_messages.append(f"[PARAM] authorized_signatory_name: {authorized_signatory_name}")
        print(f"[PARAM] remarks: {remarks}")
        api_messages.append(f"[PARAM] remarks: {remarks}")
        print(f"[FILE] cancelled_cheque_url: {cancelled_cheque_url.filename if cancelled_cheque_url else None}")
        api_messages.append(f"[FILE] cancelled_cheque_url: {cancelled_cheque_url.filename if cancelled_cheque_url else None}")
        print(f"[FILE] excise_license_url: {excise_license_url.filename if excise_license_url else None}")
        api_messages.append(f"[FILE] excise_license_url: {excise_license_url.filename if excise_license_url else None}")
        print(f"[FILE] trade_license_url: {trade_license_url.filename if trade_license_url else None}")
        api_messages.append(f"[FILE] trade_license_url: {trade_license_url.filename if trade_license_url else None}")
        print(f"[FILE] shop_establishment_license_url: {shop_establishment_license_url.filename if shop_establishment_license_url else None}")
        api_messages.append(f"[FILE] shop_establishment_license_url: {shop_establishment_license_url.filename if shop_establishment_license_url else None}")
        print(f"[FILE] gst_certificate_url: {gst_certificate_url.filename if gst_certificate_url else None}")
        api_messages.append(f"[FILE] gst_certificate_url: {gst_certificate_url.filename if gst_certificate_url else None}")
        print(f"[FILE] fire_noc_url: {fire_noc_url.filename if fire_noc_url else None}")
        api_messages.append(f"[FILE] fire_noc_url: {fire_noc_url.filename if fire_noc_url else None}")
        print(f"[FILE] shop_photo_url: {shop_photo_url_file.filename if shop_photo_url_file else None}")
        api_messages.append(f"[FILE] shop_photo_url: {shop_photo_url_file.filename if shop_photo_url_file else None}")
        
        # Create new retailer instance
        print(f"\n[STEP] Creating new retailer")
        api_messages.append("[STEP] Creating new retailer")
        new_retailer = Retailer(
            shop_name=shop_name,
            license_type=license_type,
            excise_license_no=excise_license_no,
            license_issuing_authority=license_issuing_authority,
            license_valid_from=license_valid_from,
            license_valid_upto=license_valid_upto,
            gst_no=gst_no,
            pan_no=pan_no,
            owner_name=owner_name,
            ownership_type=ownership_type,
            registered_address=registered_address,
            opening_time=opening_time,
            closing_time=closing_time,
            bank_name=bank_name,
            bank_ac_no=bank_ac_no,
            ifsc_code=ifsc_code,
            bank_branch_name=bank_branch_name,
            upi_id=upi_id,
            phn_no=phn_no,
            alt_phn=alt_phn,
            email=email,
            authorized_signatory_name=authorized_signatory_name,
            remarks=remarks,
        )
        print(f"[SUCCESS] Retailer instance created")
        api_messages.append("[SUCCESS] Retailer instance created")
        
        # Add to database to get retailer_id
        print(f"[STEP] Adding retailer to database")
        api_messages.append("[STEP] Adding retailer to database")
        db.add(new_retailer)
        db.flush()
        print(f"[SUCCESS] Retailer added to database with ID: {new_retailer.retailer_id}")
        api_messages.append(f"[SUCCESS] Retailer added to database with ID: {new_retailer.retailer_id}")
        
        # Create upload directory
        print(f"[STEP] Creating upload directory for retailer_id: {new_retailer.retailer_id}")
        api_messages.append(f"[STEP] Creating upload directory for retailer_id: {new_retailer.retailer_id}")
        upload_path = create_upload_directory(new_retailer.retailer_id)
        print(f"[SUCCESS] Upload directory created at: {upload_path}")
        api_messages.append(f"[SUCCESS] Upload directory created at: {upload_path}")
        
        # Save required files
        print(f"\n[STEP] Starting file uploads processing")
        api_messages.append("[STEP] Starting file uploads processing")
        
        if not validate_file(cancelled_cheque_url):
            raise HTTPException(status_code=400, detail="Invalid file format for cancelled cheque")
        print(f"[PROCESS] Uploading cancelled_cheque_url: {cancelled_cheque_url.filename}")
        api_messages.append(f"[PROCESS] Uploading cancelled_cheque_url: {cancelled_cheque_url.filename}")
        new_retailer.cancelled_cheque_url = save_file(cancelled_cheque_url, upload_path, "cancelled_cheque")
        print(f"[SUCCESS] cancelled_cheque_url saved at: {new_retailer.cancelled_cheque_url}")
        api_messages.append(f"[SUCCESS] cancelled_cheque_url saved")
        
        if not validate_file(excise_license_url):
            raise HTTPException(status_code=400, detail="Invalid file format for excise license")
        print(f"[PROCESS] Uploading excise_license_url: {excise_license_url.filename}")
        api_messages.append(f"[PROCESS] Uploading excise_license_url: {excise_license_url.filename}")
        new_retailer.excise_license_url = save_file(excise_license_url, upload_path, "excise_license")
        print(f"[SUCCESS] excise_license_url saved at: {new_retailer.excise_license_url}")
        api_messages.append(f"[SUCCESS] excise_license_url saved")
        
        if not validate_file(trade_license_url):
            raise HTTPException(status_code=400, detail="Invalid file format for trade license")
        print(f"[PROCESS] Uploading trade_license_url: {trade_license_url.filename}")
        api_messages.append(f"[PROCESS] Uploading trade_license_url: {trade_license_url.filename}")
        new_retailer.trade_license_url = save_file(trade_license_url, upload_path, "trade_license")
        print(f"[SUCCESS] trade_license_url saved at: {new_retailer.trade_license_url}")
        api_messages.append(f"[SUCCESS] trade_license_url saved")
        
        if not validate_file(shop_establishment_license_url):
            raise HTTPException(status_code=400, detail="Invalid file format for shop establishment license")
        print(f"[PROCESS] Uploading shop_establishment_license_url: {shop_establishment_license_url.filename}")
        api_messages.append(f"[PROCESS] Uploading shop_establishment_license_url: {shop_establishment_license_url.filename}")
        new_retailer.shop_establishment_license_url = save_file(shop_establishment_license_url, upload_path, "shop_establishment_license")
        print(f"[SUCCESS] shop_establishment_license_url saved at: {new_retailer.shop_establishment_license_url}")
        api_messages.append(f"[SUCCESS] shop_establishment_license_url saved")
        
        if not validate_file(gst_certificate_url):
            raise HTTPException(status_code=400, detail="Invalid file format for GST certificate")
        print(f"[PROCESS] Uploading gst_certificate_url: {gst_certificate_url.filename}")
        api_messages.append(f"[PROCESS] Uploading gst_certificate_url: {gst_certificate_url.filename}")
        new_retailer.gst_certificate_url = save_file(gst_certificate_url, upload_path, "gst_certificate")
        print(f"[SUCCESS] gst_certificate_url saved at: {new_retailer.gst_certificate_url}")
        api_messages.append(f"[SUCCESS] gst_certificate_url saved")
        
        if not validate_file(fire_noc_url):
            raise HTTPException(status_code=400, detail="Invalid file format for fire NOC")
        print(f"[PROCESS] Uploading fire_noc_url: {fire_noc_url.filename}")
        api_messages.append(f"[PROCESS] Uploading fire_noc_url: {fire_noc_url.filename}")
        new_retailer.fire_noc_url = save_file(fire_noc_url, upload_path, "fire_noc")
        print(f"[SUCCESS] fire_noc_url saved at: {new_retailer.fire_noc_url}")
        api_messages.append(f"[SUCCESS] fire_noc_url saved")
        
        # Save optional file
        if shop_photo_url_file and validate_file(shop_photo_url_file):
            print(f"[PROCESS] Uploading shop_photo_url: {shop_photo_url_file.filename}")
            api_messages.append(f"[PROCESS] Uploading shop_photo_url: {shop_photo_url_file.filename}")
            new_retailer.shop_photo_url = save_file(shop_photo_url_file, upload_path, "shop_photo")
            print(f"[SUCCESS] shop_photo_url saved at: {new_retailer.shop_photo_url}")
            api_messages.append(f"[SUCCESS] shop_photo_url saved")
        
        # Commit changes
        print(f"\n[STEP] Committing changes to database")
        api_messages.append("[STEP] Committing changes to database")
        db.commit()
        print(f"[SUCCESS] Database transaction committed")
        api_messages.append("[SUCCESS] Database transaction committed")
        
        # Refresh to get latest data
        print(f"[STEP] Refreshing retailer record from database")
        api_messages.append("[STEP] Refreshing retailer record from database")
        db.refresh(new_retailer)
        print(f"[SUCCESS] Retailer record refreshed")
        api_messages.append("[SUCCESS] Retailer record refreshed")
        
        print(f"\n[FINAL] Retailer registration completed successfully!")
        api_messages.append("[FINAL] Retailer registration completed successfully!")
        print(f"[RESULT] Retailer ID: {new_retailer.retailer_id}")
        api_messages.append(f"[RESULT] Retailer ID: {new_retailer.retailer_id}")
        print(f"[RESULT] Shop Name: {new_retailer.shop_name}")
        api_messages.append(f"[RESULT] Shop Name: {new_retailer.shop_name}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Your retailer registration request has been submitted successfully and is pending verification. We will review your application and notify you of the status within 3-5 business days.",
            "retailer_id": new_retailer.retailer_id,
            "shop_name": new_retailer.shop_name,
            "api_logs": api_messages
        }
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"=== ERROR IN CREATE RETAILER ===")
        print(f"{'='*60}")
        print(f"[ERROR] Error Type: {type(e).__name__}")
        print(f"[ERROR] Error Message: {str(e)}")
        print(f"{'='*60}\n")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Get all retailers endpoint
@router.get("/get-all", response_model=list)
async def get_all_retailers(db: Session = Depends(get_db)):
    # Get all retailers
    try:
        retailers = db.query(Retailer).all()
        return retailers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a retailer by ID endpoint
@router.get("/get-by/{retailer_id}", response_model=dict)
async def get_retailer_by_id(retailer_id: int, db: Session = Depends(get_db)):
    # Get retailer by ID
    try:
        retailer = db.query(Retailer).filter(Retailer.retailer_id == retailer_id).first()
        if not retailer:
            raise HTTPException(status_code=404, detail="Retailer not found")
        return retailer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update a retailer by ID endpoint
@router.put("/update-by/{retailer_id}", response_model=dict)
async def update_retailer(
    retailer_id: int,
    # Optional text fields for update
    shop_name: Optional[str] = Form(None),
    license_type: Optional[str] = Form(None),
    excise_license_no: Optional[str] = Form(None),
    license_issuing_authority: Optional[str] = Form(None),
    license_valid_from: Optional[str] = Form(None),
    license_valid_upto: Optional[str] = Form(None),
    gst_no: Optional[str] = Form(None),
    pan_no: Optional[str] = Form(None),
    owner_name: Optional[str] = Form(None),
    ownership_type: Optional[str] = Form(None),
    registered_address: Optional[str] = Form(None),
    opening_time: Optional[str] = Form(None),
    closing_time: Optional[str] = Form(None),
    bank_name: Optional[str] = Form(None),
    bank_ac_no: Optional[str] = Form(None),
    ifsc_code: Optional[str] = Form(None),
    bank_branch_name: Optional[str] = Form(None),
    upi_id: Optional[str] = Form(None),
    phn_no: Optional[str] = Form(None),
    alt_phn: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    authorized_signatory_name: Optional[str] = Form(None),
    remarks: Optional[str] = Form(None),
    # Optional file uploads
    cancelled_cheque_url: Optional[UploadFile] = File(None),
    excise_license_url: Optional[UploadFile] = File(None),
    trade_license_url: Optional[UploadFile] = File(None),
    shop_establishment_license_url: Optional[UploadFile] = File(None),
    gst_certificate_url: Optional[UploadFile] = File(None),
    fire_noc_url: Optional[UploadFile] = File(None),
    shop_photo_url_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Update retailer record with all fields including file uploads
    try:
        # Log update request
        print(f"\n{'='*60}")
        print(f"=== UPDATE RETAILER REQUEST (ID: {retailer_id}) ===")
        print(f"{'='*60}")
        print(f"[INFO] Request started for updating retailer_id: {retailer_id}")
        
        # Retrieve retailer record
        print(f"\n[STEP] Fetching retailer record from database")
        retailer = db.query(Retailer).filter(Retailer.retailer_id == retailer_id).first()
        if not retailer:
            print(f"[ERROR] Retailer with ID {retailer_id} not found")
            raise HTTPException(status_code=404, detail="Retailer not found")
        print(f"[SUCCESS] Retailer record found")
        
        # Update text fields
        print(f"\n[STEP] Updating text fields")
        if shop_name:
            print(f"[UPDATE] shop_name: {shop_name}")
            retailer.shop_name = shop_name
        if license_type:
            print(f"[UPDATE] license_type: {license_type}")
            retailer.license_type = license_type
        if excise_license_no:
            retailer.excise_license_no = excise_license_no
        if license_issuing_authority:
            retailer.license_issuing_authority = license_issuing_authority
        if license_valid_from:
            retailer.license_valid_from = license_valid_from
        if license_valid_upto:
            retailer.license_valid_upto = license_valid_upto
        if gst_no:
            retailer.gst_no = gst_no
        if pan_no:
            retailer.pan_no = pan_no
        if owner_name:
            retailer.owner_name = owner_name
        if ownership_type:
            retailer.ownership_type = ownership_type
        if registered_address:
            retailer.registered_address = registered_address
        if opening_time:
            retailer.opening_time = opening_time
        if closing_time:
            retailer.closing_time = closing_time
        if bank_name:
            retailer.bank_name = bank_name
        if bank_ac_no:
            retailer.bank_ac_no = bank_ac_no
        if ifsc_code:
            retailer.ifsc_code = ifsc_code
        if bank_branch_name:
            retailer.bank_branch_name = bank_branch_name
        if upi_id:
            retailer.upi_id = upi_id
        if phn_no:
            retailer.phn_no = phn_no
        if alt_phn:
            retailer.alt_phn = alt_phn
        if email:
            retailer.email = email
        if authorized_signatory_name:
            retailer.authorized_signatory_name = authorized_signatory_name
        if remarks:
            retailer.remarks = remarks
        print(f"[SUCCESS] All text fields updated")
        
        # Create upload directory path
        upload_path = f"./uploads/retailers/{retailer_id}"
        
        # Update file uploads and replace old files
        print(f"\n[STEP] Starting file uploads update processing")
        
        if cancelled_cheque_url and validate_file(cancelled_cheque_url):
            print(f"[PROCESS] Updating cancelled_cheque_url: {cancelled_cheque_url.filename}")
            retailer.cancelled_cheque_url = save_file(cancelled_cheque_url, upload_path, "cancelled_cheque")
            print(f"[SUCCESS] cancelled_cheque_url replaced")
        
        if excise_license_url and validate_file(excise_license_url):
            print(f"[PROCESS] Updating excise_license_url: {excise_license_url.filename}")
            retailer.excise_license_url = save_file(excise_license_url, upload_path, "excise_license")
            print(f"[SUCCESS] excise_license_url replaced")
        
        if trade_license_url and validate_file(trade_license_url):
            print(f"[PROCESS] Updating trade_license_url: {trade_license_url.filename}")
            retailer.trade_license_url = save_file(trade_license_url, upload_path, "trade_license")
            print(f"[SUCCESS] trade_license_url replaced")
        
        if shop_establishment_license_url and validate_file(shop_establishment_license_url):
            print(f"[PROCESS] Updating shop_establishment_license_url: {shop_establishment_license_url.filename}")
            retailer.shop_establishment_license_url = save_file(shop_establishment_license_url, upload_path, "shop_establishment_license")
            print(f"[SUCCESS] shop_establishment_license_url replaced")
        
        if gst_certificate_url and validate_file(gst_certificate_url):
            print(f"[PROCESS] Updating gst_certificate_url: {gst_certificate_url.filename}")
            retailer.gst_certificate_url = save_file(gst_certificate_url, upload_path, "gst_certificate")
            print(f"[SUCCESS] gst_certificate_url replaced")
        
        if fire_noc_url and validate_file(fire_noc_url):
            print(f"[PROCESS] Updating fire_noc_url: {fire_noc_url.filename}")
            retailer.fire_noc_url = save_file(fire_noc_url, upload_path, "fire_noc")
            print(f"[SUCCESS] fire_noc_url replaced")
        
        if shop_photo_url_file and validate_file(shop_photo_url_file):
            print(f"[PROCESS] Updating shop_photo_url: {shop_photo_url_file.filename}")
            retailer.shop_photo_url = save_file(shop_photo_url_file, upload_path, "shop_photo")
            print(f"[SUCCESS] shop_photo_url replaced")
        
        # Commit changes
        print(f"\n[STEP] Committing changes to database")
        db.commit()
        print(f"[SUCCESS] Database transaction committed")
        
        # Refresh to get latest data
        print(f"[STEP] Refreshing retailer record from database")
        db.refresh(retailer)
        print(f"[SUCCESS] Retailer record refreshed")
        
        print(f"\n[FINAL] Retailer update completed successfully!")
        print(f"[RESULT] Retailer ID: {retailer.retailer_id}")
        print(f"[RESULT] Shop Name: {retailer.shop_name}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Retailer updated successfully",
            "retailer_id": retailer.retailer_id,
            "shop_name": retailer.shop_name,
            "api_logs": [
                f"[INFO] Update request started for retailer_id: {retailer_id}",
                "[STEP] Fetching retailer record from database",
                "[SUCCESS] Retailer record found",
                "[STEP] Updating text fields",
                "[SUCCESS] All text fields updated (if provided)",
                "[STEP] Starting file uploads update processing",
                "[SUCCESS] All file uploads processed (if provided)",
                "[STEP] Committing changes to database",
                "[SUCCESS] Database transaction committed",
                "[SUCCESS] Retailer record refreshed",
                "[FINAL] Retailer update completed successfully!"
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"=== ERROR IN UPDATE RETAILER (ID: {retailer_id}) ===")
        print(f"{'='*60}")
        print(f"[ERROR] Error Type: {type(e).__name__}")
        print(f"[ERROR] Error Message: {str(e)}")
        print(f"{'='*60}\n")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Delete a retailer by ID endpoint
@router.delete("/delete-by/{retailer_id}", response_model=dict)
async def delete_retailer(retailer_id: int, db: Session = Depends(get_db)):
    # Delete retailer and associated files
    try:
        retailer = db.query(Retailer).filter(Retailer.retailer_id == retailer_id).first()
        if not retailer:
            raise HTTPException(status_code=404, detail="Retailer not found")
        
        # Delete files
        delete_retailer_files(retailer_id)
        
        # Delete database record
        db.delete(retailer)
        db.commit()
        
        return {"status": "success", "message": "Retailer deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
