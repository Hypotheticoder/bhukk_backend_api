from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db import get_db
from models.contact.contact_models import BhukkContact

router = APIRouter(prefix="/api/bhukk_contacts", tags=["bhukk_contacts"])


@router.post("/post", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_bhukk_contact(
    payload: dict,
    db: Session = Depends(get_db)
):
    try:
        # Validate required fields
        required_fields = ["name", "email", "subject", "message"]
        for field in required_fields:
            if field not in payload or not payload[field]:
                raise HTTPException(
                    status_code=400,
                    detail=f"'{field}' is required."
                )

        new_contact = BhukkContact(
            name=payload["name"],
            email=payload["email"],
            subject=payload["subject"],
            message=payload["message"],
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)

        return {
            "status": "success",
            "message": "Contact form submitted successfully.",
            "id": new_contact.id,
            "name": new_contact.name,
            "email": new_contact.email,
            "subject": new_contact.subject,
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get", response_model=list)
async def list_bhukk_contacts(limit: int = 100, db: Session = Depends(get_db)):
    try:
        contacts = db.query(BhukkContact).order_by(BhukkContact.created_at.desc()).limit(limit).all()
        return [
            {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "subject": c.subject,
                "message": c.message,
                "created_at": str(c.created_at) if c.created_at else None,
            }
            for c in contacts
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
