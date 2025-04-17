import uuid
from datetime import datetime

class Patient:
    """Patient model for storing patient information"""
    
    def __init__(self, id=None, medical_record_number=None, name=None, gender=None, 
                 birth_date=None, address=None, phone=None, id_number=None, 
                 insurance_number=None, insurance_provider=None, blood_type=None, 
                 allergies=None, emergency_contact=None, registration_date=None, **kwargs):
        self.id = id or str(uuid.uuid4())
        self.medical_record_number = medical_record_number or f"MRN-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        self.name = name
        self.gender = gender
        self.birth_date = birth_date
        self.address = address
        self.phone = phone
        self.id_number = id_number
        self.insurance_number = insurance_number
        self.insurance_provider = insurance_provider
        self.blood_type = blood_type
        self.allergies = allergies or []
        self.emergency_contact = emergency_contact or {}
        self.registration_date = registration_date or datetime.now().isoformat()
        
        # Add any additional fields from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def calculate_age(self):
        """Calculate patient age based on birth date"""
        if not self.birth_date:
            return None
        
        birth_date = datetime.fromisoformat(self.birth_date.replace('Z', '+00:00'))
        today = datetime.now()
        age = today.year - birth_date.year
        
        # Adjust age if birthday hasn't occurred yet this year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
            
        return age
    
    def to_dict(self):
        """Convert patient object to dictionary"""
        return self.__dict__
