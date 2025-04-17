import uuid
from datetime import datetime

class User:
    """User model for storing staff and doctor information"""
    
    def __init__(self, id=None, username=None, password=None, name=None, role=None, 
                 department_id=None, specialization=None, email=None, phone=None, 
                 active=True, created_at=None, last_login=None, **kwargs):
        self.id = id or str(uuid.uuid4())
        self.username = username
        self.password = password  # In production, should be hashed
        self.name = name
        self.role = role  # doctor, nurse, admin, receptionist, pharmacist, lab, etc.
        self.department_id = department_id
        self.specialization = specialization
        self.email = email
        self.phone = phone
        self.active = active
        self.created_at = created_at or datetime.now().isoformat()
        self.last_login = last_login
        
        # Add any additional fields from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = datetime.now().isoformat()
    
    def is_doctor(self):
        """Check if user is a doctor"""
        return self.role == "doctor"
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return self.__dict__
