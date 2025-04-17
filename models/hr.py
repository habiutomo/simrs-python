"""
Human Resources models for SIMRS
This module defines models related to employees and HR management.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
import enum

from app import db

class EmployeeStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"
    RETIRED = "retired"
    PROBATION = "probation"

class EmploymentType(enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    CONSULTANT = "consultant"

class Employee(db.Model):
    """
    Employee model for storing employee information
    """
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(String(20), unique=True, nullable=False)  # Employee ID/Number
    name = Column(String(255), nullable=False)
    gender = Column(String(10))
    date_of_birth = Column(Date)
    national_id = Column(String(20))  # NIK / KTP
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(100))
    
    # Employment details
    department_id = Column(Integer, ForeignKey('departments.id'))
    position = Column(String(100))
    employment_type = Column(Enum(EmploymentType), default=EmploymentType.FULL_TIME)
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE)
    join_date = Column(Date)
    end_date = Column(Date)  # End date for contract employees or retirement date
    
    # Education and professional details
    education = Column(String(100))
    professional_license_number = Column(String(50))  # STR/SIP for medical staff
    license_expiry_date = Column(Date)
    specialization = Column(String(100))
    experience_years = Column(Integer)
    
    # Emergency contact
    emergency_contact_name = Column(String(255))
    emergency_contact_phone = Column(String(20))
    emergency_contact_relation = Column(String(50))
    
    # Bank details for payroll
    bank_name = Column(String(100))
    bank_account = Column(String(50))
    bank_account_name = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    department = relationship("Department", backref="employees")
    contracts = relationship("EmployeeContract", backref="employee", lazy="dynamic")
    leaves = relationship("EmployeeLeave", backref="employee", lazy="dynamic")
    documents = relationship("EmployeeDocument", backref="employee", lazy="dynamic")
    payroll_records = relationship("PayrollRecord", backref="employee", lazy="dynamic")
    
    def __repr__(self):
        return f"<Employee {self.employee_id} - {self.name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'name': self.name,
            'gender': self.gender,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d') if self.date_of_birth else None,
            'national_id': self.national_id,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'department_id': self.department_id,
            'position': self.position,
            'employment_type': self.employment_type.value if self.employment_type else None,
            'status': self.status.value if self.status else None,
            'join_date': self.join_date.strftime('%Y-%m-%d') if self.join_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'education': self.education,
            'professional_license_number': self.professional_license_number,
            'license_expiry_date': self.license_expiry_date.strftime('%Y-%m-%d') if self.license_expiry_date else None,
            'specialization': self.specialization,
            'experience_years': self.experience_years,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone,
            'emergency_contact_relation': self.emergency_contact_relation,
            'bank_name': self.bank_name,
            'bank_account': self.bank_account,
            'bank_account_name': self.bank_account_name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    def age(self):
        """Calculate employee age based on date of birth"""
        if self.date_of_birth:
            today = datetime.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    def years_of_service(self):
        """Calculate years of service based on join date"""
        if self.join_date:
            today = datetime.now().date()
            return today.year - self.join_date.year - ((today.month, today.day) < (self.join_date.month, self.join_date.day))
        return None

class EmployeeContract(db.Model):
    """
    Employee Contract Information
    """
    __tablename__ = 'employee_contracts'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    contract_number = Column(String(50), unique=True)
    contract_type = Column(String(50))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    base_salary = Column(Float)
    allowances = Column(Float)
    position = Column(String(100))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    signed_date = Column(Date)
    attachment_path = Column(String(255))  # File path for contract document
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<EmployeeContract {self.contract_number}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'contract_number': self.contract_number,
            'contract_type': self.contract_type,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'base_salary': self.base_salary,
            'allowances': self.allowances,
            'position': self.position,
            'description': self.description,
            'is_active': self.is_active,
            'signed_date': self.signed_date.strftime('%Y-%m-%d') if self.signed_date else None,
            'attachment_path': self.attachment_path,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class LeaveType(enum.Enum):
    ANNUAL = "annual"
    SICK = "sick"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    BEREAVEMENT = "bereavement"
    UNPAID = "unpaid"
    OTHER = "other"

class LeaveStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class EmployeeLeave(db.Model):
    """
    Employee Leave Requests and Records
    """
    __tablename__ = 'employee_leaves'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    leave_type = Column(Enum(LeaveType), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_days = Column(Integer)
    reason = Column(Text)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)
    approved_by = Column(Integer)  # Reference to approving manager/supervisor
    approval_date = Column(DateTime)
    rejection_reason = Column(Text)
    attachment_path = Column(String(255))  # For medical certificates, etc.
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<EmployeeLeave {self.id} - {self.employee_id}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'leave_type': self.leave_type.value if self.leave_type else None,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'total_days': self.total_days,
            'reason': self.reason,
            'status': self.status.value if self.status else None,
            'approved_by': self.approved_by,
            'approval_date': self.approval_date.strftime('%Y-%m-%d %H:%M:%S') if self.approval_date else None,
            'rejection_reason': self.rejection_reason,
            'attachment_path': self.attachment_path,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class DocumentType(enum.Enum):
    IDENTITY = "identity"
    EDUCATION = "education"
    PROFESSIONAL = "professional"
    CONTRACT = "contract"
    PERFORMANCE = "performance"
    OTHER = "other"

class EmployeeDocument(db.Model):
    """
    Employee Documents
    """
    __tablename__ = 'employee_documents'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    file_path = Column(String(255), nullable=False)
    file_type = Column(String(50))  # PDF, DOC, JPG, etc.
    file_size = Column(Integer)  # Size in KB
    issue_date = Column(Date)
    expiry_date = Column(Date)
    is_verified = Column(Boolean, default=False)
    verified_by = Column(Integer)
    verified_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<EmployeeDocument {self.id} - {self.title}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'document_type': self.document_type.value if self.document_type else None,
            'title': self.title,
            'description': self.description,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'issue_date': self.issue_date.strftime('%Y-%m-%d') if self.issue_date else None,
            'expiry_date': self.expiry_date.strftime('%Y-%m-%d') if self.expiry_date else None,
            'is_verified': self.is_verified,
            'verified_by': self.verified_by,
            'verified_at': self.verified_at.strftime('%Y-%m-%d %H:%M:%S') if self.verified_at else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }