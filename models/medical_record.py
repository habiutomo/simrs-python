import uuid
from datetime import datetime

class MedicalRecord:
    """Medical Record model for storing patient health information"""
    
    def __init__(self, id=None, patient_id=None, doctor_id=None, visit_date=None, 
                 chief_complaint=None, diagnosis=None, treatment=None, prescriptions=None, 
                 lab_results=None, vitals=None, notes=None, follow_up=None,
                 created_at=None, updated_at=None, record_type=None, **kwargs):
        self.id = id or str(uuid.uuid4())
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.visit_date = visit_date or datetime.now().isoformat()
        self.chief_complaint = chief_complaint
        self.diagnosis = diagnosis or []
        self.treatment = treatment
        self.prescriptions = prescriptions or []
        self.lab_results = lab_results or []
        self.vitals = vitals or {}
        self.notes = notes
        self.follow_up = follow_up
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or self.created_at
        self.record_type = record_type or "outpatient"  # outpatient, inpatient, emergency
        
        # Add any additional fields from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def add_prescription(self, medication, dosage, frequency, duration, instructions=None):
        """Add a prescription to the medical record"""
        prescription = {
            "medication": medication,
            "dosage": dosage,
            "frequency": frequency,
            "duration": duration,
            "instructions": instructions,
            "prescribed_at": datetime.now().isoformat()
        }
        self.prescriptions.append(prescription)
        self.updated_at = datetime.now().isoformat()
    
    def add_lab_result(self, test_name, result, reference_range=None, notes=None):
        """Add a lab result to the medical record"""
        lab_result = {
            "test_name": test_name,
            "result": result,
            "reference_range": reference_range,
            "notes": notes,
            "recorded_at": datetime.now().isoformat()
        }
        self.lab_results.append(lab_result)
        self.updated_at = datetime.now().isoformat()
    
    def update_vitals(self, blood_pressure=None, heart_rate=None, temperature=None, 
                      respiratory_rate=None, oxygen_saturation=None, height=None, weight=None):
        """Update patient vitals"""
        vitals = {
            "recorded_at": datetime.now().isoformat()
        }
        
        if blood_pressure:
            vitals["blood_pressure"] = blood_pressure
        if heart_rate:
            vitals["heart_rate"] = heart_rate
        if temperature:
            vitals["temperature"] = temperature
        if respiratory_rate:
            vitals["respiratory_rate"] = respiratory_rate
        if oxygen_saturation:
            vitals["oxygen_saturation"] = oxygen_saturation
        if height:
            vitals["height"] = height
        if weight:
            vitals["weight"] = weight
            
        self.vitals = vitals
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert medical record object to dictionary"""
        return self.__dict__
