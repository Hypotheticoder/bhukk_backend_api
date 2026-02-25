from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Optional
from models.terms_conditions.terms_conditions_models import TermsConditions
from db import get_db

router = APIRouter(prefix="/api/terms-conditions", tags=["terms-conditions"])

# Create Terms & Conditions endpoint
@router.post("/create", response_model=dict)
async def create_terms_conditions(
    # Required fields
    headline: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    # Create new terms & conditions record
    try:
        # Log all received parameters
        print(f"\n{'='*60}")
        print(f"=== CREATE TERMS & CONDITIONS REQUEST ===")
        print(f"{'='*60}")
        print(f"[INFO] Request started for creating new terms & conditions")
        print(f"[PARAM] headline: {headline}")
        print(f"[PARAM] description: {description}")
        
        # Create new terms & conditions instance
        print(f"\n[STEP] Creating new terms & conditions instance")
        new_terms_conditions = TermsConditions(
            headline=headline,
            description=description,
        )
        print(f"[SUCCESS] Terms & Conditions instance created")
        
        # Add to database
        print(f"[STEP] Adding terms & conditions to database")
        db.add(new_terms_conditions)
        db.commit()
        print(f"[SUCCESS] Database transaction committed")
        
        # Refresh to get latest data
        print(f"[STEP] Refreshing terms & conditions record from database")
        db.refresh(new_terms_conditions)
        print(f"[SUCCESS] Terms & Conditions record refreshed")
        
        print(f"\n[FINAL] Terms & Conditions creation completed successfully!")
        print(f"[RESULT] ID: {new_terms_conditions.id}")
        print(f"[RESULT] Headline: {new_terms_conditions.headline}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Terms & Conditions created successfully",
            "id": new_terms_conditions.id,
            "headline": new_terms_conditions.headline,
        }
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"=== ERROR IN CREATE TERMS & CONDITIONS ===")
        print(f"{'='*60}")
        print(f"[ERROR] Error Type: {type(e).__name__}")
        print(f"[ERROR] Error Message: {str(e)}")
        print(f"{'='*60}\n")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Get all terms & conditions endpoint
@router.get("/get-all", response_model=list)
async def get_all_terms_conditions(db: Session = Depends(get_db)):
    # Get all terms & conditions
    try:
        terms_conditions = db.query(TermsConditions).all()
        return terms_conditions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get terms & conditions by ID endpoint
@router.get("/get-by/{tc_id}", response_model=dict)
async def get_terms_conditions_by_id(tc_id: int, db: Session = Depends(get_db)):
    # Get terms & conditions by ID
    try:
        terms_conditions = db.query(TermsConditions).filter(TermsConditions.id == tc_id).first()
        if not terms_conditions:
            raise HTTPException(status_code=404, detail="Terms & Conditions not found")
        return terms_conditions
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update terms & conditions by ID endpoint
@router.put("/update-by/{tc_id}", response_model=dict)
async def update_terms_conditions(
    tc_id: int,
    # Optional fields for update
    headline: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Update terms & conditions record
    try:
        print(f"\n{'='*60}")
        print(f"=== UPDATE TERMS & CONDITIONS REQUEST (ID: {tc_id}) ===")
        print(f"{'='*60}")
        print(f"[INFO] Update request started for terms & conditions id: {tc_id}")
        
        # Fetch terms & conditions record from database
        print(f"[STEP] Fetching terms & conditions record from database")
        terms_conditions = db.query(TermsConditions).filter(TermsConditions.id == tc_id).first()
        if not terms_conditions:
            raise HTTPException(status_code=404, detail="Terms & Conditions not found")
        print(f"[SUCCESS] Terms & Conditions record found")
        
        # Update fields
        print(f"[STEP] Updating fields")
        if headline:
            print(f"[UPDATE] headline: {headline}")
            terms_conditions.headline = headline
        if description:
            print(f"[UPDATE] description: {description}")
            terms_conditions.description = description
        print(f"[SUCCESS] All fields updated")
        
        # Commit changes
        print(f"\n[STEP] Committing changes to database")
        db.commit()
        print(f"[SUCCESS] Database transaction committed")
        
        # Refresh to get latest data
        print(f"[STEP] Refreshing terms & conditions record from database")
        db.refresh(terms_conditions)
        print(f"[SUCCESS] Terms & Conditions record refreshed")
        
        print(f"\n[FINAL] Terms & Conditions update completed successfully!")
        print(f"[RESULT] ID: {terms_conditions.id}")
        print(f"[RESULT] Headline: {terms_conditions.headline}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Terms & Conditions updated successfully",
            "id": terms_conditions.id,
            "headline": terms_conditions.headline,
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"=== ERROR IN UPDATE TERMS & CONDITIONS (ID: {tc_id}) ===")
        print(f"{'='*60}")
        print(f"[ERROR] Error Type: {type(e).__name__}")
        print(f"[ERROR] Error Message: {str(e)}")
        print(f"{'='*60}\n")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Delete terms & conditions by ID endpoint
@router.delete("/delete-by/{tc_id}", response_model=dict)
async def delete_terms_conditions(tc_id: int, db: Session = Depends(get_db)):
    # Delete terms & conditions record
    try:
        terms_conditions = db.query(TermsConditions).filter(TermsConditions.id == tc_id).first()
        if not terms_conditions:
            raise HTTPException(status_code=404, detail="Terms & Conditions not found")
        
        # Delete database record
        db.delete(terms_conditions)
        db.commit()
        
        return {"message": "Terms & Conditions deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
