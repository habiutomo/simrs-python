import logging
from app import app, db

# Setup debugging
logging.basicConfig(level=logging.DEBUG)

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    init_db()  # Initialize database tables
    app.run(host="0.0.0.0", port=5000, debug=True)