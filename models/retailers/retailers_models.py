from sqlalchemy import Column, Integer, String, DateTime, Text, Time
from sqlalchemy.sql import func
from db import Base

class Retailer(Base):
    # Table name in database
    __tablename__ = "retailers"

    # Primary key
    retailer_id = Column(Integer, primary_key=True, index=True)

    # Shop details (Required)
    shop_name = Column(String(255), nullable=False, index=True)
    
    # License details
    license_type = Column(String(50), nullable=True)
    excise_license_no = Column(String(50), nullable=True)
    license_issuing_authority = Column(String(255), nullable=False)
    license_valid_from = Column(String(50), nullable=False)
    license_valid_upto = Column(String(50), nullable=False)
    
    # Tax and compliance
    gst_no = Column(String(20), nullable=True)
    pan_no = Column(String(20), nullable=True)
    
    # Owner details
    owner_name = Column(String(255), nullable=True)
    ownership_type = Column(String(50), nullable=True)
    
    # Address details (Required)
    registered_address = Column(Text, nullable=False)
    
    # Shop details
    shop_photo_url = Column(Text, nullable=True)
    opening_time = Column(String(20), nullable=True)
    closing_time = Column(String(20), nullable=True)
    
    # Bank details (Required)
    bank_name = Column(String(255), nullable=False)
    bank_ac_no = Column(String(30), nullable=False)
    ifsc_code = Column(String(20), nullable=False)
    bank_branch_name = Column(String(255), nullable=True)
    upi_id = Column(String(100), nullable=True)
    
    # Contact details (Required)
    phn_no = Column(String(20), nullable=False)
    alt_phn = Column(String(20), nullable=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    
    # Authorization details
    authorized_signatory_name = Column(String(255), nullable=True)
    
    # File uploads (Required)
    cancelled_cheque_url = Column(Text, nullable=False)
    excise_license_url = Column(Text, nullable=False)
    trade_license_url = Column(Text, nullable=False)
    shop_establishment_license_url = Column(Text, nullable=False)
    gst_certificate_url = Column(Text, nullable=False)
    fire_noc_url = Column(Text, nullable=False)
    
    # Status and remarks
    verification_status = Column(String(50), default="pending", nullable=False)
    rejection_reason = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
