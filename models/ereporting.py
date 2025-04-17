
from datetime import datetime
from app import db

class ReportConfig(db.Model):
    """E-Reporting Configuration"""
    id = db.Column(db.Integer, primary_key=True)
    report_code = db.Column(db.String(50))  # RL1, RL2, etc
    report_name = db.Column(db.String(100))
    api_url = db.Column(db.String(200))
    api_key = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    schedule = db.Column(db.String(50))  # daily/weekly/monthly/quarterly
    last_submitted = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ReportSubmission(db.Model):
    """Report Submission History"""
    id = db.Column(db.Integer, primary_key=True)
    report_code = db.Column(db.String(50))
    period = db.Column(db.String(20))  # e.g. 2025-Q1, 2025-01
    data = db.Column(db.JSON)
    status = db.Column(db.String(20))  # draft/submitted/accepted/rejected
    submitted_at = db.Column(db.DateTime)
    response_message = db.Column(db.Text)
