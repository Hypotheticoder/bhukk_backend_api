from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from db import Base

class TermsConditions(Base):
    # Table name in database
    __tablename__ = "terms_conditions"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Terms & Conditions details
    headline = Column(String(2055), nullable=False, index=True)
    description = Column(Text, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
