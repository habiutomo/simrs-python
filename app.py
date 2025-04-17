import os
import logging
from flask import Flask, session, request, g
from datetime import datetime
import json
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "simrs-development-key")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simrs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Setup Babel for internationalization
try:
    from flask_babel import Babel
    babel = Babel(app)
except ImportError:
    logging.warning("Flask-Babel not available, internationalization disabled")
    babel = None

# Import models and routes after app is initialized
from routes.main_routes import main_bp
from routes.api_routes import api_bp

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(api_bp, url_prefix='/api')


@app.before_request
def before_request():
    # Log activity
    if request.endpoint and not request.endpoint.startswith('static'):
        with app.app_context():
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'endpoint': request.endpoint,
                'method': request.method,
                'ip': request.remote_addr
            }
            # Add db logging logic if you have a suitable logging table
            #db.session.add(LogEntry(**log_entry)) # Example, adapt to your LogEntry model
            #db.session.commit()
            print(f"Logged activity: {log_entry}") # temporary logging to console


# Configure locale selector function
def get_locale():
    # Use locale from URL parameters, user settings, or accept-language header
    locale = request.args.get('locale')
    if locale:
        session['locale'] = locale
    return session.get('locale', request.accept_languages.best_match(['id', 'en']))

# Set the locale selector function based on version
try:
    babel.init_app(app, locale_selector=get_locale)
except TypeError:
    # Fallback for older Flask-Babel versions
    babel.localeselector(get_locale)

# Save data to file before shutting down
@app.teardown_appcontext
def teardown_appcontext(exception):
    pass # removed data store save, assuming db handles persistence

# Load data from file when starting -  removed data store loading, assuming db handles initialization
with app.app_context():
    db.create_all() # Create tables if they don't exist