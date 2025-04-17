
from app import db
from models.bpjs import BPJSCredential, BPJSApiLog, BPJSVerificationLog, BPJSReferral, BPJSSEP, BPJSClaim

def init_db():
    """Initialize database tables"""
    try:
        # Create all tables
        db.create_all()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")

if __name__ == "__main__":
    init_db()
