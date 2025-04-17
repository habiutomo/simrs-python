import uuid
from datetime import datetime

class Appointment:
    """Appointment model for scheduling patient visits"""
    
    def __init__(self, id=None, patient_id=None, doctor_id=None, department_id=None, 
                 appointment_date=None, appointment_time=None, reason=None, status=None, 
                 notes=None, created_at=None, **kwargs):
        self.id = id or str(uuid.uuid4())
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.department_id = department_id
        
        # If appointment_date doesn't include time, combine with appointment_time
        if appointment_date and appointment_time and 'T' not in appointment_date:
            self.appointment_date = f"{appointment_date}T{appointment_time}"
        else:
            self.appointment_date = appointment_date
        
        self.appointment_time = appointment_time
        self.reason = reason
        self.status = status or "scheduled"  # scheduled, completed, cancelled, no-show
        self.notes = notes
        self.created_at = created_at or datetime.now().isoformat()
        
        # Add any additional fields from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def is_today(self):
        """Check if appointment is scheduled for today"""
        if not self.appointment_date:
            return False
        
        appointment_date = self.appointment_date.split('T')[0]
        today = datetime.now().strftime('%Y-%m-%d')
        return appointment_date == today
    
    def to_dict(self):
        """Convert appointment object to dictionary"""
        return self.__dict__
