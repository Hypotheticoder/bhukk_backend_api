from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from db import Base

class Partner(Base):
    # Table name in database
    __tablename__ = "partners"

    # Primary key
    partner_id = Column(Integer, primary_key=True, index=True)

    # Partner details (Required)
    partner_name = Column(String(255), nullable=False, index=True)
    partner_tagline = Column(String(255), nullable=True)
    partner_description = Column(Text, nullable=True)
    partner_website = Column(String(1555), nullable=True)
    
    # Partner URL (file upload - required)
    partner_url = Column(Text, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
