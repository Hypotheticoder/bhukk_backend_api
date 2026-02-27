from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
import uuid
from db import Base

def gen_uuid():
    return str(uuid.uuid4())
from sqlalchemy.sql import func
from db import Base

from sqlalchemy.sql import func
from db import Base


class Partner(Base):
    __tablename__ = "partners"

    partner_id = Column(Integer, primary_key=True, index=True)

    # System-generated UUID
    delivery_partner_id = Column(String(36), default=gen_uuid, unique=True, nullable=False, index=True)

    # Personal details
    full_name = Column(String(255), nullable=False)
    date_of_birth = Column(String(50), nullable=True)
    gender = Column(String(20), nullable=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone_no = Column(String(20), nullable=False)
    alt_phone_no = Column(String(20), nullable=True)
    password = Column(String(255), nullable=False)
    profile_photo_url = Column(Text, nullable=True)

    # ID proof
    id_proof_type = Column(String(50), nullable=True)
    id_proof_url = Column(Text, nullable=True)

    # Address
    address_line = Column(Text, nullable=True)

    # Vehicle details
    vehicle_type = Column(String(50), nullable=True)
    vehicle_model = Column(String(255), nullable=True)
    vehicle_number = Column(String(100), nullable=True)
    vehicle_rc_url = Column(Text, nullable=True)

    # Driving license
    driving_license_number = Column(String(100), nullable=True)
    driving_license_url = Column(Text, nullable=True)

    # Servicing zones
    servicing_zones = Column(Text, nullable=True)

    # Toggles and flags
    is_active_for_delivery = Column(String(10), default="true", nullable=False)
    chakna_enabled = Column(String(10), default="false", nullable=False)
    food_trade_license_available = Column(String(10), default="false", nullable=False)
    fssai_number = Column(String(100), nullable=True)

    # Bank details
    bank_account_name = Column(String(255), nullable=True)
    bank_name = Column(String(255), nullable=True)
    account_number = Column(String(50), nullable=True)
    ifsc_code = Column(String(50), nullable=True)
    upi_id = Column(String(100), nullable=True)
    cancelled_cheque_url = Column(Text, nullable=True)

    # Onboarding, status and metadata
    onboarding_status = Column(String(50), default="Pending", nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    account_status = Column(String(50), default="Active", nullable=False)
    remarks = Column(Text, nullable=True)
