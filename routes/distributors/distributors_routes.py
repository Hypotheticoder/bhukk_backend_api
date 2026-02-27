from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Optional, List
from models.distributors.distributors_models import Distributor
from services.distributors.distributors_file_uploads import (
    create_upload_directory, save_file, delete_distributor_files, validate_file
)
from db import get_db
import json

router = APIRouter(prefix="/api/distributors", tags=["distributors"])

# Distributor Application POST endpoint
@router.post("/create", response_model=dict)
async def create_distributor(
    # Required fields
    trade_name: str = Form(...),
    email: str = Form(...),
    phn_no: str = Form(...),
    registered_address: str = Form(...),
    bank_ac_name: str = Form(...),
    bank_ac_no: str = Form(...),
    ifsc_code: str = Form(...),
    # Required file uploads
    gst_certificate_url: UploadFile = File(...),
    pan_url: UploadFile = File(...),
    msme_certificate_url: UploadFile = File(...),
    firesafety_certificate_url: UploadFile = File(...),
    excise_license_url: UploadFile = File(...),
    company_incorporation_certificate_url: UploadFile = File(...),
    trade_license_url: UploadFile = File(...),
    cancelled_cheque_url: UploadFile = File(...),
    transporation_logistics_url: UploadFile = File(...),
    # Optional fields
    business_type: Optional[str] = Form(None),
    gst_no: Optional[str] = Form(None),
    pan_no: Optional[str] = Form(None),
    tan_no: Optional[str] = Form(None),
    msme_registered: Optional[bool] = Form(None),
    warehouse_address: Optional[str] = Form(None),
    warehouse_license_no: Optional[str] = Form(None),
    excise_license_no: Optional[str] = Form(None),
    license_valid_from: Optional[str] = Form(None),
    license_valid_upto: Optional[str] = Form(None),
    bank_branch_name: Optional[str] = Form(None),
    upi_id: Optional[str] = Form(None),
    delivery_fleet_size: Optional[int] = Form(None),
    servicing_area: Optional[str] = Form(None),
    contact_person_name: Optional[str] = Form(None),
    alt_phn_no: Optional[str] = Form(None),
    vehicle_count: Optional[int] = Form(None),
    remarks: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Create new distributor record
    try:
        # Log all received parameters
        print(f"\n{'='*60}")
        print(f"=== CREATE DISTRIBUTOR REQUEST ===")
        print(f"{'='*60}")
        print(f"[INFO] Request started for creating new distributor")
        print(f"[PARAM] trade_name: {trade_name}")
        print(f"[PARAM] email: {email}")
        print(f"[PARAM] phn_no: {phn_no}")
        print(f"[PARAM] registered_address: {registered_address}")
        print(f"[PARAM] bank_ac_name: {bank_ac_name}")
        print(f"[PARAM] bank_ac_no: {bank_ac_no}")
        print(f"[PARAM] ifsc_code: {ifsc_code}")
        print(f"[PARAM] business_type: {business_type}")
        print(f"[PARAM] gst_no: {gst_no}")
        print(f"[PARAM] pan_no: {pan_no}")
        print(f"[PARAM] tan_no: {tan_no}")
        print(f"[PARAM] msme_registered: {msme_registered}")
        print(f"[PARAM] warehouse_address: {warehouse_address}")
        print(f"[PARAM] warehouse_license_no: {warehouse_license_no}")
        print(f"[PARAM] excise_license_no: {excise_license_no}")
        print(f"[PARAM] license_valid_from: {license_valid_from}")
        print(f"[PARAM] license_valid_upto: {license_valid_upto}")
        print(f"[PARAM] bank_branch_name: {bank_branch_name}")
        print(f"[PARAM] upi_id: {upi_id}")
        print(f"[PARAM] delivery_fleet_size: {delivery_fleet_size}")
        print(f"[PARAM] servicing_area: {servicing_area}")
        print(f"[PARAM] contact_person_name: {contact_person_name}")
        print(f"[PARAM] alt_phn_no: {alt_phn_no}")
        print(f"[PARAM] vehicle_count: {vehicle_count}")
        print(f"[PARAM] remarks: {remarks}")
        print(f"[FILE] gst_certificate_url: {gst_certificate_url.filename if gst_certificate_url else None}")
        print(f"[FILE] pan_url: {pan_url.filename if pan_url else None}")
        print(f"[FILE] msme_certificate_url: {msme_certificate_url.filename if msme_certificate_url else None}")
        print(f"[FILE] firesafety_certificate_url: {firesafety_certificate_url.filename if firesafety_certificate_url else None}")
        print(f"[FILE] excise_license_url: {excise_license_url.filename if excise_license_url else None}")
        print(f"[FILE] company_incorporation_certificate_url: {company_incorporation_certificate_url.filename if company_incorporation_certificate_url else None}")
        print(f"[FILE] trade_license_url: {trade_license_url.filename if trade_license_url else None}")
        print(f"[FILE] cancelled_cheque_url: {cancelled_cheque_url.filename if cancelled_cheque_url else None}")
        print(f"[FILE] transporation_logistics_url: {transporation_logistics_url.filename if transporation_logistics_url else None}")
        
        # Parse servicing_area JSON if provided
        servicing_area_json = None
        if servicing_area:
            try:
                servicing_area_json = json.loads(servicing_area)
            except:
                raise HTTPException(status_code=400, detail="Invalid servicing_area JSON format")
        
        # Create new distributor instance
        print(f"\n[STEP] Creating new distributor instance")
        new_distributor = Distributor(
            trade_name=trade_name,
            email=email,
            phn_no=phn_no,
            registered_address=registered_address,
            bank_ac_name=bank_ac_name,
            bank_ac_no=bank_ac_no,
            ifsc_code=ifsc_code,
            business_type=business_type,
            gst_no=gst_no,
            pan_no=pan_no,
            tan_no=tan_no,
            msme_registered=msme_registered,
            warehouse_address=warehouse_address,
            warehouse_license_no=warehouse_license_no,
            excise_license_no=excise_license_no,
            license_valid_from=license_valid_from,
            license_valid_upto=license_valid_upto,
            bank_branch_name=bank_branch_name,
            upi_id=upi_id,
            delivery_fleet_size=delivery_fleet_size,
            servicing_area=servicing_area_json,
            contact_person_name=contact_person_name,
            alt_phn_no=alt_phn_no,
            vehicle_count=vehicle_count,
            remarks=remarks,
            # Initialize non-nullable file URL columns so INSERT/flush won't fail
            gst_certificate_url="",
            pan_url="",
            msme_certificate_url="",
            firesafety_certificate_url="",
            excise_license_url="",
            company_incorporation_certificate_url="",
            trade_license_url="",
            cancelled_cheque_url="",
            transporation_logistics_url="",
        )
        print(f"[SUCCESS] Distributor instance created")
        
        # Add to database to get distributor_id
        print(f"[STEP] Adding distributor to database")
        db.add(new_distributor)
        db.flush()
        print(f"[SUCCESS] Distributor added to database with ID: {new_distributor.distributor_id}")
        
        # Create upload directory
        print(f"[STEP] Creating upload directory for distributor_id: {new_distributor.distributor_id}")
        upload_path = create_upload_directory(new_distributor.distributor_id)
        print(f"[SUCCESS] Upload directory created at: {upload_path}")
        
        # Save required files
        print(f"\n[STEP] Starting file uploads processing")
        
        if not validate_file(gst_certificate_url):
            raise HTTPException(status_code=400, detail="Invalid file format for GST certificate")
        print(f"[PROCESS] Uploading gst_certificate_url: {gst_certificate_url.filename}")
        new_distributor.gst_certificate_url = save_file(gst_certificate_url, upload_path, "gst_certificate")
        print(f"[SUCCESS] gst_certificate_url saved at: {new_distributor.gst_certificate_url}")
        
        if not validate_file(pan_url):
            raise HTTPException(status_code=400, detail="Invalid file format for PAN URL")
        print(f"[PROCESS] Uploading pan_url: {pan_url.filename}")
        new_distributor.pan_url = save_file(pan_url, upload_path, "pan_document")
        print(f"[SUCCESS] pan_url saved at: {new_distributor.pan_url}")
        
        if not validate_file(msme_certificate_url):
            raise HTTPException(status_code=400, detail="Invalid file format for MSME certificate")
        print(f"[PROCESS] Uploading msme_certificate_url: {msme_certificate_url.filename}")
        new_distributor.msme_certificate_url = save_file(msme_certificate_url, upload_path, "msme_certificate")
        print(f"[SUCCESS] msme_certificate_url saved at: {new_distributor.msme_certificate_url}")
        
        if not validate_file(firesafety_certificate_url):
            raise HTTPException(status_code=400, detail="Invalid file format for fire safety certificate")
        print(f"[PROCESS] Uploading firesafety_certificate_url: {firesafety_certificate_url.filename}")
        new_distributor.firesafety_certificate_url = save_file(firesafety_certificate_url, upload_path, "firesafety_certificate")
        print(f"[SUCCESS] firesafety_certificate_url saved at: {new_distributor.firesafety_certificate_url}")
        
        if not validate_file(excise_license_url):
            raise HTTPException(status_code=400, detail="Invalid file format for excise license")
        print(f"[PROCESS] Uploading excise_license_url: {excise_license_url.filename}")
        new_distributor.excise_license_url = save_file(excise_license_url, upload_path, "excise_license")
        print(f"[SUCCESS] excise_license_url saved at: {new_distributor.excise_license_url}")
        
        if not validate_file(company_incorporation_certificate_url):
            raise HTTPException(status_code=400, detail="Invalid file format for company incorporation certificate")
        print(f"[PROCESS] Uploading company_incorporation_certificate_url: {company_incorporation_certificate_url.filename}")
        new_distributor.company_incorporation_certificate_url = save_file(company_incorporation_certificate_url, upload_path, "incorporation_cert")
        print(f"[SUCCESS] company_incorporation_certificate_url saved at: {new_distributor.company_incorporation_certificate_url}")
        
        if not validate_file(trade_license_url):
            raise HTTPException(status_code=400, detail="Invalid file format for trade license")
        print(f"[PROCESS] Uploading trade_license_url: {trade_license_url.filename}")
        new_distributor.trade_license_url = save_file(trade_license_url, upload_path, "trade_license")
        print(f"[SUCCESS] trade_license_url saved at: {new_distributor.trade_license_url}")
        
        if not validate_file(cancelled_cheque_url):
            raise HTTPException(status_code=400, detail="Invalid file format for cancelled cheque")
        print(f"[PROCESS] Uploading cancelled_cheque_url: {cancelled_cheque_url.filename}")
        new_distributor.cancelled_cheque_url = save_file(cancelled_cheque_url, upload_path, "cancelled_cheque")
        print(f"[SUCCESS] cancelled_cheque_url saved at: {new_distributor.cancelled_cheque_url}")
        
        if not validate_file(transporation_logistics_url):
            raise HTTPException(status_code=400, detail="Invalid file format for transportation logistics")
        print(f"[PROCESS] Uploading transporation_logistics_url: {transporation_logistics_url.filename}")
        new_distributor.transporation_logistics_url = save_file(transporation_logistics_url, upload_path, "transporation_logistics")
        print(f"[SUCCESS] transporation_logistics_url saved at: {new_distributor.transporation_logistics_url}")
        
        # Commit changes
        print(f"\n[STEP] Committing changes to database")
        db.commit()
        print(f"[SUCCESS] Database transaction committed")
        
        # Refresh to get latest data
        print(f"[STEP] Refreshing distributor record from database")
        db.refresh(new_distributor)
        print(f"[SUCCESS] Distributor record refreshed")
        
        print(f"\n[FINAL] Distributor registration completed successfully!")
        print(f"[RESULT] Distributor ID: {new_distributor.distributor_id}")
        print(f"[RESULT] Trade Name: {new_distributor.trade_name}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Your distributor registration request has been submitted successfully and is pending verification. We will review your application and notify you of the status within 3-5 business days.",
            "distributor_id": new_distributor.distributor_id,
            "trade_name": new_distributor.trade_name,
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"=== ERROR IN CREATE DISTRIBUTOR ===")
        print(f"{'='*60}")
        print(f"[ERROR] Error Type: {type(e).__name__}")
        print(f"[ERROR] Error Message: {str(e)}")
        print(f"{'='*60}\n")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Get all distributors endpoint
@router.get("/get-all", response_model=list)
async def get_all_distributors(db: Session = Depends(get_db)):
    # Get all distributors
    try:
        distributors = db.query(Distributor).all()
        return distributors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a distributor's application by ID endpoint
@router.get("/get-by/{distributor_id}", response_model=dict)
async def get_distributor_by_id(distributor_id: int, db: Session = Depends(get_db)):
    # Get distributor by ID
    try:
        distributor = db.query(Distributor).filter(Distributor.distributor_id == distributor_id).first()
        if not distributor:
            raise HTTPException(status_code=404, detail="Distributor not found")
        return distributor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update a distributor's application by ID endpoint
@router.put("/update-by/{distributor_id}", response_model=dict)
async def update_distributor(
    distributor_id: int,
    # Optional text fields for update
    trade_name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phn_no: Optional[str] = Form(None),
    registered_address: Optional[str] = Form(None),
    bank_ac_name: Optional[str] = Form(None),
    bank_ac_no: Optional[str] = Form(None),
    ifsc_code: Optional[str] = Form(None),
    business_type: Optional[str] = Form(None),
    gst_no: Optional[str] = Form(None),
    pan_no: Optional[str] = Form(None),
    tan_no: Optional[str] = Form(None),
    msme_registered: Optional[bool] = Form(None),
    warehouse_address: Optional[str] = Form(None),
    warehouse_license_no: Optional[str] = Form(None),
    excise_license_no: Optional[str] = Form(None),
    license_valid_from: Optional[str] = Form(None),
    license_valid_upto: Optional[str] = Form(None),
    bank_branch_name: Optional[str] = Form(None),
    upi_id: Optional[str] = Form(None),
    delivery_fleet_size: Optional[int] = Form(None),
    servicing_area: Optional[str] = Form(None),
    contact_person_name: Optional[str] = Form(None),
    alt_phn_no: Optional[str] = Form(None),
    vehicle_count: Optional[int] = Form(None),
    remarks: Optional[str] = Form(None),
    # Optional file uploads
    gst_certificate_url: Optional[UploadFile] = File(None),
    pan_url: Optional[UploadFile] = File(None),
    msme_certificate_url: Optional[UploadFile] = File(None),
    firesafety_certificate_url: Optional[UploadFile] = File(None),
    excise_license_url: Optional[UploadFile] = File(None),
    company_incorporation_certificate_url: Optional[UploadFile] = File(None),
    trade_license_url: Optional[UploadFile] = File(None),
    cancelled_cheque_url: Optional[UploadFile] = File(None),
    transporation_logistics_url: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Update distributor record
    try:
        print(f"\n{'='*60}")
        print(f"=== UPDATE DISTRIBUTOR REQUEST (ID: {distributor_id}) ===")
        print(f"{'='*60}")
        print(f"[INFO] Update request started for distributor_id: {distributor_id}")
        
        # Fetch distributor record from database
        print(f"[STEP] Fetching distributor record from database")
        distributor = db.query(Distributor).filter(Distributor.distributor_id == distributor_id).first()
        if not distributor:
            raise HTTPException(status_code=404, detail="Distributor not found")
        print(f"[SUCCESS] Distributor record found")
        
        # Parse servicing_area JSON if provided
        servicing_area_json = None
        if servicing_area:
            try:
                servicing_area_json = json.loads(servicing_area)
            except:
                raise HTTPException(status_code=400, detail="Invalid servicing_area JSON format")
        
        # Update text fields
        print(f"[STEP] Updating text fields")
        if trade_name:
            print(f"[UPDATE] trade_name: {trade_name}")
            distributor.trade_name = trade_name
        if email:
            print(f"[UPDATE] email: {email}")
            distributor.email = email
        if phn_no:
            print(f"[UPDATE] phn_no: {phn_no}")
            distributor.phn_no = phn_no
        if registered_address:
            print(f"[UPDATE] registered_address: {registered_address}")
            distributor.registered_address = registered_address
        if bank_ac_name:
            print(f"[UPDATE] bank_ac_name: {bank_ac_name}")
            distributor.bank_ac_name = bank_ac_name
        if bank_ac_no:
            print(f"[UPDATE] bank_ac_no: {bank_ac_no}")
            distributor.bank_ac_no = bank_ac_no
        if ifsc_code:
            print(f"[UPDATE] ifsc_code: {ifsc_code}")
            distributor.ifsc_code = ifsc_code
        if business_type:
            print(f"[UPDATE] business_type: {business_type}")
            distributor.business_type = business_type
        if gst_no:
            print(f"[UPDATE] gst_no: {gst_no}")
            distributor.gst_no = gst_no
        if pan_no:
            print(f"[UPDATE] pan_no: {pan_no}")
            distributor.pan_no = pan_no
        if tan_no:
            print(f"[UPDATE] tan_no: {tan_no}")
            distributor.tan_no = tan_no
        if msme_registered is not None:
            print(f"[UPDATE] msme_registered: {msme_registered}")
            distributor.msme_registered = msme_registered
        if warehouse_address:
            print(f"[UPDATE] warehouse_address: {warehouse_address}")
            distributor.warehouse_address = warehouse_address
        if warehouse_license_no:
            print(f"[UPDATE] warehouse_license_no: {warehouse_license_no}")
            distributor.warehouse_license_no = warehouse_license_no
        if excise_license_no:
            print(f"[UPDATE] excise_license_no: {excise_license_no}")
            distributor.excise_license_no = excise_license_no
        if license_valid_from:
            print(f"[UPDATE] license_valid_from: {license_valid_from}")
            distributor.license_valid_from = license_valid_from
        if license_valid_upto:
            print(f"[UPDATE] license_valid_upto: {license_valid_upto}")
            distributor.license_valid_upto = license_valid_upto
        if bank_branch_name:
            print(f"[UPDATE] bank_branch_name: {bank_branch_name}")
            distributor.bank_branch_name = bank_branch_name
        if upi_id:
            print(f"[UPDATE] upi_id: {upi_id}")
            distributor.upi_id = upi_id
        if delivery_fleet_size:
            print(f"[UPDATE] delivery_fleet_size: {delivery_fleet_size}")
            distributor.delivery_fleet_size = delivery_fleet_size
        if servicing_area_json:
            print(f"[UPDATE] servicing_area: {servicing_area_json}")
            distributor.servicing_area = servicing_area_json
        if contact_person_name:
            print(f"[UPDATE] contact_person_name: {contact_person_name}")
            distributor.contact_person_name = contact_person_name
        if alt_phn_no:
            print(f"[UPDATE] alt_phn_no: {alt_phn_no}")
            distributor.alt_phn_no = alt_phn_no
        if vehicle_count:
            print(f"[UPDATE] vehicle_count: {vehicle_count}")
            distributor.vehicle_count = vehicle_count
        if remarks:
            print(f"[UPDATE] remarks: {remarks}")
            distributor.remarks = remarks
        print(f"[SUCCESS] All text fields updated")
        
        # Create upload directory path
        upload_path = f"./uploads/distributors/{distributor_id}"
        
        # Update file uploads and replace old files
        print(f"\n[STEP] Starting file uploads update processing")
        
        if gst_certificate_url and validate_file(gst_certificate_url):
            print(f"[PROCESS] Updating gst_certificate_url: {gst_certificate_url.filename}")
            old_url = distributor.gst_certificate_url
            distributor.gst_certificate_url = save_file(gst_certificate_url, upload_path, "gst_certificate")
            print(f"[SUCCESS] gst_certificate_url replaced - Old: {old_url} -> New: {distributor.gst_certificate_url}")
        
        if pan_url and validate_file(pan_url):
            print(f"[PROCESS] Updating pan_url: {pan_url.filename}")
            old_url = distributor.pan_url
            distributor.pan_url = save_file(pan_url, upload_path, "pan_document")
            print(f"[SUCCESS] pan_url replaced - Old: {old_url} -> New: {distributor.pan_url}")
        
        if msme_certificate_url and validate_file(msme_certificate_url):
            print(f"[PROCESS] Updating msme_certificate_url: {msme_certificate_url.filename}")
            old_url = distributor.msme_certificate_url
            distributor.msme_certificate_url = save_file(msme_certificate_url, upload_path, "msme_certificate")
            print(f"[SUCCESS] msme_certificate_url replaced - Old: {old_url} -> New: {distributor.msme_certificate_url}")
        
        if firesafety_certificate_url and validate_file(firesafety_certificate_url):
            print(f"[PROCESS] Updating firesafety_certificate_url: {firesafety_certificate_url.filename}")
            old_url = distributor.firesafety_certificate_url
            distributor.firesafety_certificate_url = save_file(firesafety_certificate_url, upload_path, "firesafety_certificate")
            print(f"[SUCCESS] firesafety_certificate_url replaced - Old: {old_url} -> New: {distributor.firesafety_certificate_url}")
        
        if excise_license_url and validate_file(excise_license_url):
            print(f"[PROCESS] Updating excise_license_url: {excise_license_url.filename}")
            old_url = distributor.excise_license_url
            distributor.excise_license_url = save_file(excise_license_url, upload_path, "excise_license")
            print(f"[SUCCESS] excise_license_url replaced - Old: {old_url} -> New: {distributor.excise_license_url}")
        
        if company_incorporation_certificate_url and validate_file(company_incorporation_certificate_url):
            print(f"[PROCESS] Updating company_incorporation_certificate_url: {company_incorporation_certificate_url.filename}")
            old_url = distributor.company_incorporation_certificate_url
            distributor.company_incorporation_certificate_url = save_file(company_incorporation_certificate_url, upload_path, "incorporation_cert")
            print(f"[SUCCESS] company_incorporation_certificate_url replaced - Old: {old_url} -> New: {distributor.company_incorporation_certificate_url}")
        
        if trade_license_url and validate_file(trade_license_url):
            print(f"[PROCESS] Updating trade_license_url: {trade_license_url.filename}")
            old_url = distributor.trade_license_url
            distributor.trade_license_url = save_file(trade_license_url, upload_path, "trade_license")
            print(f"[SUCCESS] trade_license_url replaced - Old: {old_url} -> New: {distributor.trade_license_url}")
        
        if cancelled_cheque_url and validate_file(cancelled_cheque_url):
            print(f"[PROCESS] Updating cancelled_cheque_url: {cancelled_cheque_url.filename}")
            old_url = distributor.cancelled_cheque_url
            distributor.cancelled_cheque_url = save_file(cancelled_cheque_url, upload_path, "cancelled_cheque")
            print(f"[SUCCESS] cancelled_cheque_url replaced - Old: {old_url} -> New: {distributor.cancelled_cheque_url}")
        
        if transporation_logistics_url and validate_file(transporation_logistics_url):
            print(f"[PROCESS] Updating transporation_logistics_url: {transporation_logistics_url.filename}")
            old_url = distributor.transporation_logistics_url
            distributor.transporation_logistics_url = save_file(transporation_logistics_url, upload_path, "transporation_logistics")
            print(f"[SUCCESS] transporation_logistics_url replaced - Old: {old_url} -> New: {distributor.transporation_logistics_url}")
        
        # Commit changes
        print(f"\n[STEP] Committing changes to database")
        db.commit()
        print(f"[SUCCESS] Database transaction committed")
        
        # Refresh to get latest data
        print(f"[STEP] Refreshing distributor record from database")
        db.refresh(distributor)
        print(f"[SUCCESS] Distributor record refreshed")
        
        print(f"\n[FINAL] Distributor update completed successfully!")
        print(f"[RESULT] Distributor ID: {distributor.distributor_id}")
        print(f"[RESULT] Trade Name: {distributor.trade_name}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Distributor updated successfully",
            "distributor_id": distributor.distributor_id,
            "trade_name": distributor.trade_name,
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"=== ERROR IN UPDATE DISTRIBUTOR (ID: {distributor_id}) ===")
        print(f"{'='*60}")
        print(f"[ERROR] Error Type: {type(e).__name__}")
        print(f"[ERROR] Error Message: {str(e)}")
        print(f"{'='*60}\n")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Delete a distributor's application by ID endpoint
@router.delete("/delete-by/{distributor_id}", response_model=dict)
async def delete_distributor(distributor_id: int, db: Session = Depends(get_db)):
    # Delete distributor and associated files
    try:
        distributor = db.query(Distributor).filter(Distributor.distributor_id == distributor_id).first()
        if not distributor:
            raise HTTPException(status_code=404, detail="Distributor not found")
        
        # Delete files
        delete_distributor_files(distributor_id)
        
        # Delete database record
        db.delete(distributor)
        db.commit()
        
        return {"message": "Distributor deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
