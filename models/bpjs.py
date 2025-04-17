"""
BPJS Kesehatan models for SIMRS
This module defines models related to BPJS Kesehatan integration.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship

from app import db

class BPJSCredential(db.Model):
    """
    BPJS API Credentials storage
    """
    __tablename__ = 'bpjs_credentials'
    
    id = Column(Integer, primary_key=True)
    cons_id = Column(String(255), nullable=False)
    secret_key = Column(String(255), nullable=False)
    user_key = Column(String(255), nullable=False)
    environment = Column(String(20), default='development')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<BPJSCredential {self.id}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'cons_id': self.cons_id,
            'secret_key': self.secret_key,
            'user_key': self.user_key,
            'environment': self.environment,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class BPJSVerificationLog(db.Model):
    """
    Logs for BPJS membership verification
    """
    __tablename__ = 'bpjs_verification_logs'
    
    id = Column(Integer, primary_key=True)
    search_type = Column(String(10), nullable=False)  # 'noka' or 'nik'
    search_value = Column(String(20), nullable=False)  # card number or NIK
    service_date = Column(String(10))  # format: YYYY-MM-DD
    response_code = Column(String(10))
    response_message = Column(Text)
    response_data = Column(JSON)
    is_valid = Column(Boolean)
    member_name = Column(String(255))
    member_status = Column(String(20))
    member_nik = Column(String(20))
    member_card_number = Column(String(20))
    member_class = Column(String(10))
    member_type = Column(String(50))
    primary_facility = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<BPJSVerificationLog {self.id} - {self.search_value}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'search_type': self.search_type,
            'search_value': self.search_value,
            'service_date': self.service_date,
            'response_code': self.response_code,
            'response_message': self.response_message,
            'is_valid': self.is_valid,
            'member_name': self.member_name,
            'member_status': self.member_status,
            'member_nik': self.member_nik,
            'member_card_number': self.member_card_number,
            'member_class': self.member_class,
            'member_type': self.member_type,
            'primary_facility': self.primary_facility,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

class BPJSReferral(db.Model):
    """
    BPJS Referral information
    """
    __tablename__ = 'bpjs_referrals'
    
    id = Column(Integer, primary_key=True)
    referral_number = Column(String(30), nullable=False, unique=True)
    referral_type = Column(String(10))  # e.g., '1' for FKTP to FKRTL, '2' for FKRTL to FKRTL
    member_card_number = Column(String(20), nullable=False)
    member_name = Column(String(255))
    referral_date = Column(String(10))  # format: YYYY-MM-DD
    diagnosis_code = Column(String(20))
    diagnosis_name = Column(String(255))
    referring_facility_code = Column(String(20))
    referring_facility_name = Column(String(255))
    referred_facility_code = Column(String(20))
    referred_facility_name = Column(String(255))
    referral_reason = Column(Text)
    is_used = Column(Boolean, default=False)
    used_date = Column(String(10))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<BPJSReferral {self.referral_number}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'referral_number': self.referral_number,
            'referral_type': self.referral_type,
            'member_card_number': self.member_card_number,
            'member_name': self.member_name,
            'referral_date': self.referral_date,
            'diagnosis_code': self.diagnosis_code,
            'diagnosis_name': self.diagnosis_name,
            'referring_facility_code': self.referring_facility_code,
            'referring_facility_name': self.referring_facility_name,
            'referred_facility_code': self.referred_facility_code,
            'referred_facility_name': self.referred_facility_name,
            'referral_reason': self.referral_reason,
            'is_used': self.is_used,
            'used_date': self.used_date,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class BPJSSEP(db.Model):
    """
    BPJS SEP (Surat Eligibilitas Peserta) information
    """
    __tablename__ = 'bpjs_sep'
    
    id = Column(Integer, primary_key=True)
    sep_number = Column(String(30), nullable=False, unique=True)
    member_card_number = Column(String(20), nullable=False)
    member_name = Column(String(255))
    member_nik = Column(String(20))
    service_type = Column(String(10))  # '1' for outpatient, '2' for inpatient
    service_date = Column(String(10))  # format: YYYY-MM-DD
    facility_code = Column(String(20))
    facility_name = Column(String(255))
    diagnosis_code = Column(String(20))
    diagnosis_name = Column(String(255))
    referral_number = Column(String(30))
    referral_type = Column(String(10))
    doctor_code = Column(String(20))
    doctor_name = Column(String(255))
    class_code = Column(String(5))
    class_name = Column(String(20))
    status = Column(String(20), default='active')  # active, cancelled, expired
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<BPJSSEP {self.sep_number}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'sep_number': self.sep_number,
            'member_card_number': self.member_card_number,
            'member_name': self.member_name,
            'member_nik': self.member_nik,
            'service_type': self.service_type,
            'service_date': self.service_date,
            'facility_code': self.facility_code,
            'facility_name': self.facility_name,
            'diagnosis_code': self.diagnosis_code,
            'diagnosis_name': self.diagnosis_name,
            'referral_number': self.referral_number,
            'referral_type': self.referral_type,
            'doctor_code': self.doctor_code,
            'doctor_name': self.doctor_name,
            'class_code': self.class_code,
            'class_name': self.class_name,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class BPJSClaim(db.Model):
    """
    BPJS Claims information
    """
    __tablename__ = 'bpjs_claims'
    
    id = Column(Integer, primary_key=True)
    claim_number = Column(String(30), nullable=False, unique=True)
    sep_number = Column(String(30), nullable=False)
    member_card_number = Column(String(20), nullable=False)
    member_name = Column(String(255))
    service_type = Column(String(10))  # '1' for outpatient, '2' for inpatient
    service_start_date = Column(String(10))  # format: YYYY-MM-DD
    service_end_date = Column(String(10))  # format: YYYY-MM-DD
    diagnosis_codes = Column(Text)  # Comma separated diagnosis codes
    procedure_codes = Column(Text)  # Comma separated procedure codes
    claim_amount = Column(Float)
    approved_amount = Column(Float)
    status = Column(String(20))  # pending, verified, approved, returned, rejected, paid
    status_date = Column(String(10))
    rejection_reason = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<BPJSClaim {self.claim_number}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'claim_number': self.claim_number,
            'sep_number': self.sep_number,
            'member_card_number': self.member_card_number,
            'member_name': self.member_name,
            'service_type': self.service_type,
            'service_start_date': self.service_start_date,
            'service_end_date': self.service_end_date,
            'diagnosis_codes': self.diagnosis_codes,
            'procedure_codes': self.procedure_codes,
            'claim_amount': self.claim_amount,
            'approved_amount': self.approved_amount,
            'status': self.status,
            'status_date': self.status_date,
            'rejection_reason': self.rejection_reason,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class BPJSApiLog(db.Model):
    """
    Logs for BPJS API requests and responses
    """
    __tablename__ = 'bpjs_api_logs'
    
    id = Column(Integer, primary_key=True)
    endpoint = Column(Text, nullable=False)
    method = Column(String(10), nullable=False)  # GET, POST, PUT, DELETE
    service_type = Column(String(20))  # vclaim, pcare, aplicare
    request_timestamp = Column(DateTime, default=datetime.now)
    request_data = Column(JSON)
    response_code = Column(String(10))
    response_message = Column(Text)
    response_data = Column(JSON)
    execution_time = Column(Float)  # in seconds
    
    def __repr__(self):
        return f"<BPJSApiLog {self.id} - {self.endpoint}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'endpoint': self.endpoint,
            'method': self.method,
            'service_type': self.service_type,
            'request_timestamp': self.request_timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.request_timestamp else None,
            'request_data': self.request_data,
            'response_code': self.response_code,
            'response_message': self.response_message,
            'execution_time': self.execution_time
        }
from datetime import datetime
from app import db

class BPJSCredential(db.Model):
    """BPJS API Credentials"""
    id = db.Column(db.Integer, primary_key=True)
    cons_id = db.Column(db.String(50), nullable=False)
    secret_key = db.Column(db.String(100), nullable=False) 
    user_key = db.Column(db.String(100), nullable=False)
    service_name = db.Column(db.String(50))  # vclaim, aplicare, etc
    environment = db.Column(db.String(20))  # development/production
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class BPJSApiLog(db.Model):
    """BPJS API Request/Response Logs"""
    id = db.Column(db.Integer, primary_key=True)
    request_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    endpoint = db.Column(db.String(100))
    request_data = db.Column(db.JSON)
    response_data = db.Column(db.JSON)
    response_code = db.Column(db.String(10))
    is_success = db.Column(db.Boolean)
