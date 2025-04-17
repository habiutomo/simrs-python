
from datetime import datetime
from app import db

class RadiologySystem(db.Model):
    """Radiology System Configuration""" 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    api_url = db.Column(db.String(200))
    api_key = db.Column(db.String(100))
    pacs_url = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class RadiologyOrder(db.Model):
    """Radiology Orders"""
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exam_code = db.Column(db.String(50))
    exam_name = db.Column(db.String(100))
    priority = db.Column(db.String(20))  # routine/urgent/stat
    status = db.Column(db.String(20))  # ordered/completed/cancelled
    report_text = db.Column(db.Text)
    image_urls = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
