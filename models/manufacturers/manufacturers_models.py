from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from db import Base

class Manufacturer(Base):
    # Table name in database
    __tablename__ = "manufacturers"

    # Primary key
    manufacturer_id = Column(Integer, primary_key=True, index=True)

    # Company details (Required)
    company_name = Column(String(255), nullable=False, index=True)
    
    # Incorporation certificate
    incorporation_certificate_url = Column(Text, nullable=False)
    
    # Tax details
    pan_no = Column(String(20), nullable=True)
    pan_url = Column(Text, nullable=False)
    gst_no = Column(String(20), nullable=True)
    gst_cert_url = Column(Text, nullable=False)
    
    # Address details
    registered_office_address = Column(Text, nullable=False)
    factory_address = Column(Text, nullable=True)
    
    # Regulatory licenses
    excise_no = Column(String(50), nullable=True)
    excise_license_url = Column(Text, nullable=False)
    fssai_license_no = Column(String(50), nullable=True)
    fssai_license_url = Column(Text, nullable=False)
    trade_license_url = Column(Text, nullable=False)
    
    # Authority signatory
    auth_signatory_name = Column(String(255), nullable=True)
    auth_letter_url = Column(Text, nullable=False)
    
    # Company images (JSON array of URLs)
    manufacturer_images_url = Column(JSON, nullable=False)
    
    # Bank details (Required)
    bank_name = Column(String(255), nullable=False)
    bank_ac_no = Column(String(30), nullable=False)
    ifsc_code = Column(String(20), nullable=False)
    cancelled_cheque_url = Column(Text, nullable=False)
    upi_id = Column(String(100), nullable=True)
    
    # Contact details (Required)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phn_no = Column(String(20), nullable=False)
    alt_phn_no = Column(String(20), nullable=True)
    
    # Verification and timestamps
    verification_status = Column(String(50), default="pending", nullable=False)
    rejection_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
