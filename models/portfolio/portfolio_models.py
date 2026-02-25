from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from db import Base

class Portfolio(Base):
    # Table name in database
    __tablename__ = "portfolio"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Company details
    mission = Column(Text, nullable=True)
    vision = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    director_message = Column(Text, nullable=True)
    
    # Team members (JSON format: {image_url, name, designation, message})
    developer1 = Column(JSON, nullable=True)
    developer2 = Column(JSON, nullable=True)
    director = Column(JSON, nullable=True)
    marketing_head_1 = Column(JSON, nullable=True)
    marketing_head_2 = Column(JSON, nullable=True)
    senior_graphics_designer = Column(JSON, nullable=True)
    
    # Counts
    distributors_count = Column(Integer, nullable=True, default=0)
    retailers_count = Column(Integer, nullable=True, default=0)
    manufacturers_count = Column(Integer, nullable=True, default=0)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
