from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Optional
from models.partners.partners_models import Partner
from services.partners.partners_file_uploads import (
    create_upload_directory, save_file, delete_partner_files, validate_file
)
from db import get_db

router = APIRouter(prefix="/api/partners", tags=["partners"])

# Create Partner endpoint
@router.post("/create", response_model=dict)
async def create_partner(
    # Required fields
    partner_name: str = Form(...),
    partner_url: UploadFile = File(...),
    # Optional fields
    partner_tagline: Optional[str] = Form(None),
    partner_description: Optional[str] = Form(None),
    partner_website: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Create new partner record
    try:
        # Log all received parameters
        print(f"\n{'='*60}")
        print(f"=== CREATE PARTNER REQUEST ===")
        print(f"{'='*60}")
        print(f"[INFO] Request started for creating new partner")
        print(f"[PARAM] partner_name: {partner_name}")
        print(f"[PARAM] partner_tagline: {partner_tagline}")
        print(f"[PARAM] partner_description: {partner_description}")
        print(f"[PARAM] partner_website: {partner_website}")
        print(f"[FILE] partner_url: {partner_url.filename if partner_url else None}")
        
        # Create new partner instance
        print(f"\n[STEP] Creating new partner instance")
        new_partner = Partner(
            partner_name=partner_name,
            partner_tagline=partner_tagline,
            partner_description=partner_description,
            partner_website=partner_website,
        )
        print(f"[SUCCESS] Partner instance created")
        
        # Add to database to get partner_id
        print(f"[STEP] Adding partner to database")
        db.add(new_partner)
        db.flush()
        print(f"[SUCCESS] Partner added to database with ID: {new_partner.partner_id}")
        
        # Create upload directory
        print(f"[STEP] Creating upload directory for partner_id: {new_partner.partner_id}")
        upload_path = create_upload_directory(new_partner.partner_id)
        print(f"[SUCCESS] Upload directory created at: {upload_path}")
        
        # Save partner image
        print(f"\n[STEP] Starting file upload processing")
        
        if not validate_file(partner_url):
            raise HTTPException(status_code=400, detail="Invalid file format for partner URL. Allowed formats: png, jpg, jpeg, webp, gif")
        print(f"[PROCESS] Uploading partner_url: {partner_url.filename}")
        new_partner.partner_url = save_file(partner_url, upload_path, "partner_logo")
        print(f"[SUCCESS] partner_url saved at: {new_partner.partner_url}")
        
        # Commit changes
        print(f"\n[STEP] Committing changes to database")
        db.commit()
        print(f"[SUCCESS] Database transaction committed")
        
        # Refresh to get latest data
        print(f"[STEP] Refreshing partner record from database")
        db.refresh(new_partner)
        print(f"[SUCCESS] Partner record refreshed")
        
        print(f"\n[FINAL] Partner creation completed successfully!")
        print(f"[RESULT] Partner ID: {new_partner.partner_id}")
        print(f"[RESULT] Partner Name: {new_partner.partner_name}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Partner created successfully",
            "partner_id": new_partner.partner_id,
            "partner_name": new_partner.partner_name,
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"=== ERROR IN CREATE PARTNER ===")
        print(f"{'='*60}")
        print(f"[ERROR] Error Type: {type(e).__name__}")
        print(f"[ERROR] Error Message: {str(e)}")
        print(f"{'='*60}\n")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Get all partners endpoint
@router.get("/get-all", response_model=list)
async def get_all_partners(db: Session = Depends(get_db)):
    # Get all partners
    try:
        partners = db.query(Partner).all()
        return partners
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a partner by ID endpoint
@router.get("/get-by/{partner_id}", response_model=dict)
async def get_partner_by_id(partner_id: int, db: Session = Depends(get_db)):
    # Get partner by ID
    try:
        partner = db.query(Partner).filter(Partner.partner_id == partner_id).first()
        if not partner:
            raise HTTPException(status_code=404, detail="Partner not found")
        return partner
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update a partner by ID endpoint
@router.put("/update-by/{partner_id}", response_model=dict)
async def update_partner(
    partner_id: int,
    # Optional fields for update
    partner_name: Optional[str] = Form(None),
    partner_tagline: Optional[str] = Form(None),
    partner_description: Optional[str] = Form(None),
    partner_website: Optional[str] = Form(None),
    partner_url: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Update partner record
    try:
        print(f"\n{'='*60}")
        print(f"=== UPDATE PARTNER REQUEST (ID: {partner_id}) ===")
        print(f"{'='*60}")
        print(f"[INFO] Update request started for partner_id: {partner_id}")
        
        # Fetch partner record from database
        print(f"[STEP] Fetching partner record from database")
        partner = db.query(Partner).filter(Partner.partner_id == partner_id).first()
        if not partner:
            raise HTTPException(status_code=404, detail="Partner not found")
        print(f"[SUCCESS] Partner record found")
        
        # Update text fields
        print(f"[STEP] Updating text fields")
        if partner_name:
            print(f"[UPDATE] partner_name: {partner_name}")
            partner.partner_name = partner_name
        if partner_tagline:
            print(f"[UPDATE] partner_tagline: {partner_tagline}")
            partner.partner_tagline = partner_tagline
        if partner_description:
            print(f"[UPDATE] partner_description: {partner_description}")
            partner.partner_description = partner_description
        if partner_website:
            print(f"[UPDATE] partner_website: {partner_website}")
            partner.partner_website = partner_website
        print(f"[SUCCESS] All text fields updated")
        
        # Create upload directory path
        upload_path = f"./uploads/partners/{partner_id}"
        
        # Update file upload
        print(f"\n[STEP] Starting file upload update processing")
        
        if partner_url and validate_file(partner_url):
            print(f"[PROCESS] Updating partner_url: {partner_url.filename}")
            old_url = partner.partner_url
            partner.partner_url = save_file(partner_url, upload_path, "partner_logo")
            print(f"[SUCCESS] partner_url replaced - Old: {old_url} -> New: {partner.partner_url}")
        
        # Commit changes
        print(f"\n[STEP] Committing changes to database")
        db.commit()
        print(f"[SUCCESS] Database transaction committed")
        
        # Refresh to get latest data
        print(f"[STEP] Refreshing partner record from database")
        db.refresh(partner)
        print(f"[SUCCESS] Partner record refreshed")
        
        print(f"\n[FINAL] Partner update completed successfully!")
        print(f"[RESULT] Partner ID: {partner.partner_id}")
        print(f"[RESULT] Partner Name: {partner.partner_name}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Partner updated successfully",
            "partner_id": partner.partner_id,
            "partner_name": partner.partner_name,
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"=== ERROR IN UPDATE PARTNER (ID: {partner_id}) ===")
        print(f"{'='*60}")
        print(f"[ERROR] Error Type: {type(e).__name__}")
        print(f"[ERROR] Error Message: {str(e)}")
        print(f"{'='*60}\n")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Delete a partner by ID endpoint
@router.delete("/delete-by/{partner_id}", response_model=dict)
async def delete_partner(partner_id: int, db: Session = Depends(get_db)):
    # Delete partner and associated files
    try:
        partner = db.query(Partner).filter(Partner.partner_id == partner_id).first()
        if not partner:
            raise HTTPException(status_code=404, detail="Partner not found")
        
        # Delete files
        delete_partner_files(partner_id)
        
        # Delete database record
        db.delete(partner)
        db.commit()
        
        return {"message": "Partner deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
