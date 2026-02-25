from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean
from sqlalchemy.sql import func
from db import Base

class Distributor(Base):
    # Table name in database
    __tablename__ = "distributors"

    # Primary key
    distributor_id = Column(Integer, primary_key=True, index=True)

    # Company details (Required)
    trade_name = Column(String(1055), nullable=False, index=True)
    business_type = Column(String(1000), nullable=True)
    
    # Tax details
    gst_no = Column(String(200), nullable=True)
    gst_certificate_url = Column(Text, nullable=False)
    
    pan_no = Column(String(20), nullable=True)
    pan_url = Column(Text, nullable=False)
    
    tan_no = Column(String(20), nullable=True)
    
    # MSME details
    msme_registered = Column(Boolean, default=False, nullable=True)
    msme_certificate_url = Column(Text, nullable=False)
    
    # Address details (Required)
    registered_address = Column(Text, nullable=False)
    warehouse_address = Column(Text, nullable=True)
    
    # Warehouse and license details
    warehouse_license_no = Column(String(50), nullable=True)
    
    # Fire safety certificate
    firesafety_certificate_url = Column(Text, nullable=False)
    
    # Excise license details
    excise_license_no = Column(String(50), nullable=True)
    license_valid_from = Column(String(20), nullable=True)
    license_valid_upto = Column(String(20), nullable=True)
    excise_license_url = Column(Text, nullable=False)
    
    # Company incorporation certificate
    company_incorporation_certificate_url = Column(Text, nullable=False)
    
    # Trade license
    trade_license_url = Column(Text, nullable=False)
    
    # Bank details (Required)
    bank_ac_name = Column(String(255), nullable=False)
    bank_ac_no = Column(String(30), nullable=False)
    ifsc_code = Column(String(20), nullable=False)
    bank_branch_name = Column(String(255), nullable=True)
    cancelled_cheque_url = Column(Text, nullable=False)
    
    upi_id = Column(String(100), nullable=True)
    
    # Fleet and logistics
    delivery_fleet_size = Column(Integer, nullable=True)
    servicing_area = Column(JSON, nullable=True)
    vehicle_count = Column(Integer, nullable=True)
    transporation_logistics_url = Column(Text, nullable=False)
    
    # Contact details (Required)
    contact_person_name = Column(String(255), nullable=True)
    phn_no = Column(String(20), nullable=False)
    alt_phn_no = Column(String(20), nullable=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    
    # Verification and remarks
    verification_status = Column(String(50), default="pending", nullable=False)
    rejection_cause = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
