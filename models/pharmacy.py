
from datetime import datetime
from app import db

class PharmacySystem(db.Model):
    """Pharmacy System Configuration"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    api_url = db.Column(db.String(200))
    api_key = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DrugDispense(db.Model):
    """Drug Dispensing Records"""
    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescription.id'))
    drug_code = db.Column(db.String(50))
    drug_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    unit = db.Column(db.String(20))
    status = db.Column(db.String(20))  # pending/dispensed/cancelled
    dispensed_at = db.Column(db.DateTime)
    dispensed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
