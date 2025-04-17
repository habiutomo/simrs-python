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
from models.data_store import DataStore
from routes.main_routes import main_bp
from routes.api_routes import api_bp

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(api_bp, url_prefix='/api')

# Create global data store
data_store = DataStore()

@app.before_request
def before_request():
    g.data_store = data_store

    # Initialize data store if not already done
    if not g.data_store.is_initialized():
        g.data_store.initialize()

    # Log activity
    if request.endpoint and not request.endpoint.startswith('static'):
        g.data_store.log_activity({
            'timestamp': datetime.now().isoformat(),
            'endpoint': request.endpoint,
            'method': request.method,
            'ip': request.remote_addr
        })

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
    if hasattr(g, 'data_store'):
        g.data_store.save_to_file()

# Load data from file when starting
with app.app_context():
    # Initialize data loading
    data_store.load_from_file()