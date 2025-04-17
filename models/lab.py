
from datetime import datetime
from app import db

class LabSystem(db.Model):
    """Laboratory System Configuration"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    api_url = db.Column(db.String(200))
    api_key = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LabRequest(db.Model):
    """Laboratory Test Requests"""
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    test_code = db.Column(db.String(50))
    test_name = db.Column(db.String(100))
    priority = db.Column(db.String(20))  # normal/urgent/stat
    status = db.Column(db.String(20))  # pending/processing/completed
    result = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
