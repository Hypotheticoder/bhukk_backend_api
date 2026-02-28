from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from models.partners.partners_models import Partner
from services.partners.partners_file_uploads import (
    create_upload_directory, save_file, delete_partner_files, validate_file
)
from db import get_db
import json

router = APIRouter(prefix="/api/partners", tags=["partners"])


# Create Delivery Partner endpoint
@router.post("/create", response_model=dict)
async def create_partner(
    full_name: str = Form(...),
    date_of_birth: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    email: str = Form(...),
    phone_no: str = Form(...),
    alt_phone_no: Optional[str] = Form(None),
    password: str = Form(...),
    profile_photo_url: Optional[UploadFile] = File(None),
    id_proof_type: Optional[str] = Form(None),
    id_proof_url: Optional[UploadFile] = File(None),
    address_line: Optional[str] = Form(None),
    vehicle_type: Optional[str] = Form(None),
    vehicle_model: Optional[str] = Form(None),
    vehicle_number: Optional[str] = Form(None),
    vehicle_rc_url: Optional[UploadFile] = File(None),
    driving_license_number: Optional[str] = Form(None),
    driving_license_url: Optional[UploadFile] = File(None),
    servicing_zones: Optional[str] = Form(None),
    is_active_for_delivery: Optional[bool] = Form(True),
    chakna_enabled: Optional[bool] = Form(False),
    food_trade_license_available: Optional[bool] = Form(False),
    fssai_number: Optional[str] = Form(None),
    bank_account_name: Optional[str] = Form(None),
    bank_name: Optional[str] = Form(None),
    account_number: Optional[str] = Form(None),
    ifsc_code: Optional[str] = Form(None),
    upi_id: Optional[str] = Form(None),
    cancelled_cheque_url: Optional[UploadFile] = File(None),
    onboarding_status: Optional[str] = Form("Pending"),
    account_status: Optional[str] = Form("Active"),
    remarks: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        print(f"\n{'='*60}")
        print(f"=== CREATE DELIVERY PARTNER REQUEST ===")
        print(f"{'='*60}")

        # Check if email already exists
        existing_partner = db.query(Partner).filter(Partner.email == email).first()
        if existing_partner:
            raise HTTPException(status_code=409, detail={
                "message": f"A partner with email '{email}' already exists.",
                "duplicated_field": "email",
                "duplicated_value": email
            })

        # Check if phone number already exists
        existing_phone = db.query(Partner).filter(Partner.phone_no == phone_no).first()
        if existing_phone:
            raise HTTPException(status_code=409, detail={
                "message": f"A partner with phone number '{phone_no}' already exists.",
                "duplicated_field": "phone_no",
                "duplicated_value": phone_no
            })

        # create instance with required defaults for file/url fields to avoid NOT NULL errors
        new_partner = Partner(
            full_name=full_name,
            date_of_birth=date_of_birth,
            gender=gender,
            email=email,
            phone_no=phone_no,
            alt_phone_no=alt_phone_no,
            password=password,
            profile_photo_url="",
            id_proof_type=id_proof_type,
            id_proof_url="",
            address_line=address_line,
            vehicle_type=vehicle_type,
            vehicle_model=vehicle_model,
            vehicle_number=vehicle_number,
            vehicle_rc_url="",
            driving_license_number=driving_license_number,
            driving_license_url="",
            servicing_zones=servicing_zones,
            is_active_for_delivery=str(is_active_for_delivery).lower(),
            chakna_enabled=str(chakna_enabled).lower(),
            food_trade_license_available=str(food_trade_license_available).lower(),
            fssai_number=fssai_number,
            bank_account_name=bank_account_name,
            bank_name=bank_name,
            account_number=account_number,
            ifsc_code=ifsc_code,
            upi_id=upi_id,
            cancelled_cheque_url="",
            onboarding_status=onboarding_status,
            account_status=account_status,
            remarks=remarks,
        )

        db.add(new_partner)
        db.flush()

        upload_path = create_upload_directory(new_partner.partner_id)

        # Save files if provided
        if profile_photo_url and validate_file(profile_photo_url):
            new_partner.profile_photo_url = save_file(profile_photo_url, upload_path, "profile_photo")

        if id_proof_url and validate_file(id_proof_url):
            new_partner.id_proof_url = save_file(id_proof_url, upload_path, "id_proof")

        if vehicle_rc_url and validate_file(vehicle_rc_url):
            new_partner.vehicle_rc_url = save_file(vehicle_rc_url, upload_path, "vehicle_rc")

        if driving_license_url and validate_file(driving_license_url):
            new_partner.driving_license_url = save_file(driving_license_url, upload_path, "driving_license")

        if cancelled_cheque_url and validate_file(cancelled_cheque_url):
            new_partner.cancelled_cheque_url = save_file(cancelled_cheque_url, upload_path, "cancelled_cheque")

        # Commit and refresh
        db.commit()
        db.refresh(new_partner)

        return {"status": "success", "partner_id": new_partner.partner_id, "delivery_partner_id": new_partner.delivery_partner_id}
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig)
        if "email" in error_msg:
            raise HTTPException(status_code=409, detail={
                "message": f"A partner with email '{email}' already exists.",
                "duplicated_field": "email",
                "duplicated_value": email
            })
        elif "phone_no" in error_msg:
            raise HTTPException(status_code=409, detail={
                "message": f"A partner with phone number '{phone_no}' already exists.",
                "duplicated_field": "phone_no",
                "duplicated_value": phone_no
            })
        else:
            raise HTTPException(status_code=409, detail={
                "message": "A partner with the given details already exists.",
                "duplicated_field": "unknown",
                "duplicated_value": None
            })
    except Exception as e:
        print(f"ERROR: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Get all delivery partners
@router.get("/get-all", response_model=list)
async def get_all_partners(db: Session = Depends(get_db)):
    try:
        partners = db.query(Partner).all()
        return partners
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get delivery partner by id
@router.get("/get-by/{partner_id}", response_model=dict)
async def get_partner_by_id(partner_id: int, db: Session = Depends(get_db)):
    try:
        partner = db.query(Partner).filter(Partner.partner_id == partner_id).first()
        if not partner:
            raise HTTPException(status_code=404, detail="Partner not found")
        return partner
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Update partner
@router.put("/update-by/{partner_id}", response_model=dict)
async def update_partner(
    partner_id: int,
    full_name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone_no: Optional[str] = Form(None),
    alt_phone_no: Optional[str] = Form(None),
    profile_photo_url: Optional[UploadFile] = File(None),
    id_proof_url: Optional[UploadFile] = File(None),
    vehicle_rc_url: Optional[UploadFile] = File(None),
    driving_license_url: Optional[UploadFile] = File(None),
    cancelled_cheque_url: Optional[UploadFile] = File(None),
    onboarding_status: Optional[str] = Form(None),
    account_status: Optional[str] = Form(None),
    remarks: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        partner = db.query(Partner).filter(Partner.partner_id == partner_id).first()
        if not partner:
            raise HTTPException(status_code=404, detail="Partner not found")

        if full_name:
            partner.full_name = full_name
        if email:
            partner.email = email
        if phone_no:
            partner.phone_no = phone_no
        if alt_phone_no:
            partner.alt_phone_no = alt_phone_no
        if onboarding_status:
            partner.onboarding_status = onboarding_status
        if account_status:
            partner.account_status = account_status
        if remarks:
            partner.remarks = remarks

        upload_path = f"./uploads/partners/{partner_id}"
        if profile_photo_url and validate_file(profile_photo_url):
            partner.profile_photo_url = save_file(profile_photo_url, upload_path, "profile_photo")
        if id_proof_url and validate_file(id_proof_url):
            partner.id_proof_url = save_file(id_proof_url, upload_path, "id_proof")
        if vehicle_rc_url and validate_file(vehicle_rc_url):
            partner.vehicle_rc_url = save_file(vehicle_rc_url, upload_path, "vehicle_rc")
        if driving_license_url and validate_file(driving_license_url):
            partner.driving_license_url = save_file(driving_license_url, upload_path, "driving_license")
        if cancelled_cheque_url and validate_file(cancelled_cheque_url):
            partner.cancelled_cheque_url = save_file(cancelled_cheque_url, upload_path, "cancelled_cheque")

        db.commit()
        db.refresh(partner)
        return {"status": "success", "partner_id": partner.partner_id}
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig)
        if "email" in error_msg:
            raise HTTPException(status_code=409, detail={
                "message": f"A partner with email '{email}' already exists.",
                "duplicated_field": "email",
                "duplicated_value": email
            })
        elif "phone_no" in error_msg:
            raise HTTPException(status_code=409, detail={
                "message": f"A partner with phone number '{phone_no}' already exists.",
                "duplicated_field": "phone_no",
                "duplicated_value": phone_no
            })
        else:
            raise HTTPException(status_code=409, detail={
                "message": "A partner with the given details already exists.",
                "duplicated_field": "unknown",
                "duplicated_value": None
            })
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Delete partner
@router.delete("/delete-by/{partner_id}", response_model=dict)
async def delete_partner(partner_id: int, db: Session = Depends(get_db)):
    try:
        partner = db.query(Partner).filter(Partner.partner_id == partner_id).first()
        if not partner:
            raise HTTPException(status_code=404, detail="Partner not found")
        delete_partner_files(partner_id)
        db.delete(partner)
        db.commit()
        return {"message": "Partner deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
