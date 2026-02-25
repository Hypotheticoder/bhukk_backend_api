from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Optional
from models.portfolio.portfolio_models import Portfolio
from services.portfolio.portfolio_file_uploads import (
    save_file, validate_file
)
from db import get_db
import json

router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])

# Create Portfolio endpoint
@router.post("/create", response_model=dict)
async def create_portfolio(
    # Optional fields
    mission: Optional[str] = Form(None),
    vision: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    director_message: Optional[str] = Form(None),
    distributors_count: Optional[int] = Form(None),
    retailers_count: Optional[int] = Form(None),
    manufacturers_count: Optional[int] = Form(None),
    # Developer 1
    developer1_name: Optional[str] = Form(None),
    developer1_designation: Optional[str] = Form(None),
    developer1_message: Optional[str] = Form(None),
    developer1_image: Optional[UploadFile] = File(None),
    # Developer 2
    developer2_name: Optional[str] = Form(None),
    developer2_designation: Optional[str] = Form(None),
    developer2_message: Optional[str] = Form(None),
    developer2_image: Optional[UploadFile] = File(None),
    # Director
    director_name: Optional[str] = Form(None),
    director_designation: Optional[str] = Form(None),
    director_message_team: Optional[str] = Form(None),
    director_image: Optional[UploadFile] = File(None),
    # Marketing Head 1
    marketing_head_1_name: Optional[str] = Form(None),
    marketing_head_1_designation: Optional[str] = Form(None),
    marketing_head_1_message: Optional[str] = Form(None),
    marketing_head_1_image: Optional[UploadFile] = File(None),
    # Marketing Head 2
    marketing_head_2_name: Optional[str] = Form(None),
    marketing_head_2_designation: Optional[str] = Form(None),
    marketing_head_2_message: Optional[str] = Form(None),
    marketing_head_2_image: Optional[UploadFile] = File(None),
    # Senior Graphics Designer
    senior_graphics_designer_name: Optional[str] = Form(None),
    senior_graphics_designer_designation: Optional[str] = Form(None),
    senior_graphics_designer_message: Optional[str] = Form(None),
    senior_graphics_designer_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Create new portfolio record
    try:
        print(f"\n{'='*60}")
        print(f"=== CREATE PORTFOLIO REQUEST ===")
        print(f"{'='*60}")
        print(f"[INFO] Request started for creating new portfolio")
        
        # Create new portfolio instance
        print(f"\n[STEP] Creating new portfolio instance")
        new_portfolio = Portfolio(
            mission=mission,
            vision=vision,
            description=description,
            director_message=director_message,
            distributors_count=distributors_count,
            retailers_count=retailers_count,
            manufacturers_count=manufacturers_count,
        )
        print(f"[SUCCESS] Portfolio instance created")
        
        # Add to database to get portfolio id
        print(f"[STEP] Adding portfolio to database")
        db.add(new_portfolio)
        db.flush()
        print(f"[SUCCESS] Portfolio added to database with ID: {new_portfolio.id}")
        
        # Helper function to save team member data
        def process_team_member(name, designation, message, image_file, member_name):
            if name or designation or message or image_file:
                team_member = {}
                if name:
                    team_member["name"] = name
                if designation:
                    team_member["designation"] = designation
                if message:
                    team_member["message"] = message
                if image_file and validate_file(image_file):
                    print(f"[PROCESS] Uploading {member_name}_image: {image_file.filename}")
                    team_member["image_url"] = save_file(image_file, f"{member_name}_image")
                    print(f"[SUCCESS] {member_name} image saved at: {team_member['image_url']}")
                return team_member if team_member else None
            return None
        
        # Process team members
        print(f"\n[STEP] Processing team member data")
        
        if developer1_name or developer1_designation or developer1_message or developer1_image:
            new_portfolio.developer1 = json.dumps(process_team_member(developer1_name, developer1_designation, developer1_message, developer1_image, "developer1"))
            print(f"[SUCCESS] Developer 1 data processed")
        
        if developer2_name or developer2_designation or developer2_message or developer2_image:
            new_portfolio.developer2 = json.dumps(process_team_member(developer2_name, developer2_designation, developer2_message, developer2_image, "developer2"))
            print(f"[SUCCESS] Developer 2 data processed")
        
        if director_name or director_designation or director_message_team or director_image:
            new_portfolio.director = json.dumps(process_team_member(director_name, director_designation, director_message_team, director_image, "director"))
            print(f"[SUCCESS] Director data processed")
        
        if marketing_head_1_name or marketing_head_1_designation or marketing_head_1_message or marketing_head_1_image:
            new_portfolio.marketing_head_1 = json.dumps(process_team_member(marketing_head_1_name, marketing_head_1_designation, marketing_head_1_message, marketing_head_1_image, "marketing_head_1"))
            print(f"[SUCCESS] Marketing Head 1 data processed")
        
        if marketing_head_2_name or marketing_head_2_designation or marketing_head_2_message or marketing_head_2_image:
            new_portfolio.marketing_head_2 = json.dumps(process_team_member(marketing_head_2_name, marketing_head_2_designation, marketing_head_2_message, marketing_head_2_image, "marketing_head_2"))
            print(f"[SUCCESS] Marketing Head 2 data processed")
        
        if senior_graphics_designer_name or senior_graphics_designer_designation or senior_graphics_designer_message or senior_graphics_designer_image:
            new_portfolio.senior_graphics_designer = json.dumps(process_team_member(senior_graphics_designer_name, senior_graphics_designer_designation, senior_graphics_designer_message, senior_graphics_designer_image, "senior_graphics_designer"))
            print(f"[SUCCESS] Senior Graphics Designer data processed")
        
        # Commit changes
        print(f"\n[STEP] Committing changes to database")
        db.commit()
        print(f"[SUCCESS] Database transaction committed")
        
        # Refresh to get latest data
        print(f"[STEP] Refreshing portfolio record from database")
        db.refresh(new_portfolio)
        print(f"[SUCCESS] Portfolio record refreshed")
        
        print(f"\n[FINAL] Portfolio creation completed successfully!")
        print(f"[RESULT] Portfolio ID: {new_portfolio.id}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Portfolio created successfully",
            "id": new_portfolio.id,
        }
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"=== ERROR IN CREATE PORTFOLIO ===")
        print(f"{'='*60}")
        print(f"[ERROR] Error Type: {type(e).__name__}")
        print(f"[ERROR] Error Message: {str(e)}")
        print(f"{'='*60}\n")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Get all portfolio records endpoint
@router.get("/get-all", response_model=list)
async def get_all_portfolio(db: Session = Depends(get_db)):
    # Get all portfolio records
    try:
        portfolios = db.query(Portfolio).all()
        return portfolios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a portfolio by ID endpoint
@router.get("/get-by/{portfolio_id}", response_model=dict)
async def get_portfolio_by_id(portfolio_id: int, db: Session = Depends(get_db)):
    # Get portfolio by ID
    try:
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        return portfolio
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update a portfolio by ID endpoint
@router.put("/update-by/{portfolio_id}", response_model=dict)
async def update_portfolio(
    portfolio_id: int,
    # Optional fields
    mission: Optional[str] = Form(None),
    vision: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    director_message: Optional[str] = Form(None),
    distributors_count: Optional[int] = Form(None),
    retailers_count: Optional[int] = Form(None),
    manufacturers_count: Optional[int] = Form(None),
    # Developer 1
    developer1_name: Optional[str] = Form(None),
    developer1_designation: Optional[str] = Form(None),
    developer1_message: Optional[str] = Form(None),
    developer1_image: Optional[UploadFile] = File(None),
    # Developer 2
    developer2_name: Optional[str] = Form(None),
    developer2_designation: Optional[str] = Form(None),
    developer2_message: Optional[str] = Form(None),
    developer2_image: Optional[UploadFile] = File(None),
    # Director
    director_name: Optional[str] = Form(None),
    director_designation: Optional[str] = Form(None),
    director_message_team: Optional[str] = Form(None),
    director_image: Optional[UploadFile] = File(None),
    # Marketing Head 1
    marketing_head_1_name: Optional[str] = Form(None),
    marketing_head_1_designation: Optional[str] = Form(None),
    marketing_head_1_message: Optional[str] = Form(None),
    marketing_head_1_image: Optional[UploadFile] = File(None),
    # Marketing Head 2
    marketing_head_2_name: Optional[str] = Form(None),
    marketing_head_2_designation: Optional[str] = Form(None),
    marketing_head_2_message: Optional[str] = Form(None),
    marketing_head_2_image: Optional[UploadFile] = File(None),
    # Senior Graphics Designer
    senior_graphics_designer_name: Optional[str] = Form(None),
    senior_graphics_designer_designation: Optional[str] = Form(None),
    senior_graphics_designer_message: Optional[str] = Form(None),
    senior_graphics_designer_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Update portfolio record
    try:
        print(f"\n{'='*60}")
        print(f"=== UPDATE PORTFOLIO REQUEST (ID: {portfolio_id}) ===")
        print(f"{'='*60}")
        print(f"[INFO] Update request started for portfolio_id: {portfolio_id}")
        
        # Fetch portfolio record from database
        print(f"[STEP] Fetching portfolio record from database")
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        print(f"[SUCCESS] Portfolio record found")
        
        # Update text fields
        print(f"[STEP] Updating text fields")
        if mission:
            print(f"[UPDATE] mission: {mission}")
            portfolio.mission = mission
        if vision:
            print(f"[UPDATE] vision: {vision}")
            portfolio.vision = vision
        if description:
            print(f"[UPDATE] description: {description}")
            portfolio.description = description
        if director_message:
            print(f"[UPDATE] director_message: {director_message}")
            portfolio.director_message = director_message
        if distributors_count is not None:
            print(f"[UPDATE] distributors_count: {distributors_count}")
            portfolio.distributors_count = distributors_count
        if retailers_count is not None:
            print(f"[UPDATE] retailers_count: {retailers_count}")
            portfolio.retailers_count = retailers_count
        if manufacturers_count is not None:
            print(f"[UPDATE] manufacturers_count: {manufacturers_count}")
            portfolio.manufacturers_count = manufacturers_count
        print(f"[SUCCESS] All text fields updated")
        
        # Helper function to update team member data
        def update_team_member(existing_json, name, designation, message, image_file, member_name):
            # Parse existing data
            team_member = {}
            if existing_json:
                try:
                    team_member = json.loads(existing_json)
                except:
                    team_member = {}
            
            # Update fields
            if name:
                team_member["name"] = name
            if designation:
                team_member["designation"] = designation
            if message:
                team_member["message"] = message
            if image_file and validate_file(image_file):
                print(f"[PROCESS] Updating {member_name}_image: {image_file.filename}")
                team_member["image_url"] = save_file(image_file, f"{member_name}_image")
                print(f"[SUCCESS] {member_name} image updated at: {team_member['image_url']}")
            
            return json.dumps(team_member) if team_member else None
        
        # Process team members
        print(f"\n[STEP] Processing team member updates")
        
        if developer1_name or developer1_designation or developer1_message or developer1_image:
            portfolio.developer1 = update_team_member(portfolio.developer1, developer1_name, developer1_designation, developer1_message, developer1_image, "developer1")
            print(f"[SUCCESS] Developer 1 data updated")
        
        if developer2_name or developer2_designation or developer2_message or developer2_image:
            portfolio.developer2 = update_team_member(portfolio.developer2, developer2_name, developer2_designation, developer2_message, developer2_image, "developer2")
            print(f"[SUCCESS] Developer 2 data updated")
        
        if director_name or director_designation or director_message_team or director_image:
            portfolio.director = update_team_member(portfolio.director, director_name, director_designation, director_message_team, director_image, "director")
            print(f"[SUCCESS] Director data updated")
        
        if marketing_head_1_name or marketing_head_1_designation or marketing_head_1_message or marketing_head_1_image:
            portfolio.marketing_head_1 = update_team_member(portfolio.marketing_head_1, marketing_head_1_name, marketing_head_1_designation, marketing_head_1_message, marketing_head_1_image, "marketing_head_1")
            print(f"[SUCCESS] Marketing Head 1 data updated")
        
        if marketing_head_2_name or marketing_head_2_designation or marketing_head_2_message or marketing_head_2_image:
            portfolio.marketing_head_2 = update_team_member(portfolio.marketing_head_2, marketing_head_2_name, marketing_head_2_designation, marketing_head_2_message, marketing_head_2_image, "marketing_head_2")
            print(f"[SUCCESS] Marketing Head 2 data updated")
        
        if senior_graphics_designer_name or senior_graphics_designer_designation or senior_graphics_designer_message or senior_graphics_designer_image:
            portfolio.senior_graphics_designer = update_team_member(portfolio.senior_graphics_designer, senior_graphics_designer_name, senior_graphics_designer_designation, senior_graphics_designer_message, senior_graphics_designer_image, "senior_graphics_designer")
            print(f"[SUCCESS] Senior Graphics Designer data updated")
        
        # Commit changes
        print(f"\n[STEP] Committing changes to database")
        db.commit()
        print(f"[SUCCESS] Database transaction committed")
        
        # Refresh to get latest data
        print(f"[STEP] Refreshing portfolio record from database")
        db.refresh(portfolio)
        print(f"[SUCCESS] Portfolio record refreshed")
        
        print(f"\n[FINAL] Portfolio update completed successfully!")
        print(f"[RESULT] Portfolio ID: {portfolio.id}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Portfolio updated successfully",
            "id": portfolio.id,
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"=== ERROR IN UPDATE PORTFOLIO (ID: {portfolio_id}) ===")
        print(f"{'='*60}")
        print(f"[ERROR] Error Type: {type(e).__name__}")
        print(f"[ERROR] Error Message: {str(e)}")
        print(f"{'='*60}\n")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Delete a portfolio by ID endpoint
@router.delete("/delete-by/{portfolio_id}", response_model=dict)
async def delete_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    # Delete portfolio record
    try:
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        # Delete database record
        db.delete(portfolio)
        db.commit()
        
        return {"message": "Portfolio deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
