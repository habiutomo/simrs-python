import json
import os
import logging
from datetime import datetime, timedelta
from models.patient import Patient
from models.appointment import Appointment
from models.medical_record import MedicalRecord
from models.user import User
from models.department import Department
from models.billing import BillingRecord

class DataStore:
    """
    In-memory data storage for SIMRS application
    Acts as a replacement for a SQL database
    """
    def __init__(self):
        self.patients = {}
        self.appointments = {}
        self.medical_records = {}
        self.users = {}
        self.departments = {}
        self.billing_records = {}
        self.pharmacy_inventory = {}
        self.lab_requests = {}
        self.radiology_requests = {}
        self.inpatients = {}
        self.activities = []
        self._initialized = False
        self.data_file = 'simrs_data.json'

    def is_initialized(self):
        return self._initialized

    def initialize(self):
        """Initialize with default data if not loaded from file"""
        if not self._initialized:
            self._create_default_departments()
            self._create_default_users()
            self._initialized = True

    def _create_default_departments(self):
        """Create default departments for the hospital"""
        departments = [
            Department(id=1, name="Pediatrics", code="PED"),
            Department(id=2, name="Orthopedic", code="ORT"),
            Department(id=3, name="Dermatology", code="DER"),
            Department(id=4, name="Cardiology", code="CAR"),
            Department(id=5, name="Neurology", code="NEU"),
            Department(id=6, name="Internal Medicine", code="INT")
        ]
        for dept in departments:
            self.departments[dept.id] = dept.__dict__

    def _create_default_users(self):
        """Create default users (doctors, staff)"""
        users = [
            User(id=1, username="dr.sutono", name="Dr. Sutono", role="doctor", department_id=1),
            User(id=2, username="dr.anwijaya", name="Dr. Ani Wijaya", role="doctor", department_id=2),
            User(id=3, username="admin", name="Admin", role="admin", department_id=None)
        ]
        for user in users:
            self.users[user.id] = user.__dict__

    def add_patient(self, patient):
        """Add a new patient"""
        self.patients[patient.id] = patient.__dict__
        return patient.id

    def get_patient(self, patient_id):
        """Get patient by ID"""
        patient_data = self.patients.get(patient_id)
        if patient_data:
            return Patient(**patient_data)
        return None

    def get_all_patients(self):
        """Get all patients"""
        return [Patient(**p) for p in self.patients.values()]

    def add_appointment(self, appointment):
        """Add a new appointment"""
        self.appointments[appointment.id] = appointment.__dict__
        return appointment.id

    def get_appointment(self, appointment_id):
        """Get appointment by ID"""
        appointment_data = self.appointments.get(appointment_id)
        if appointment_data:
            return Appointment(**appointment_data)
        return None

    def get_appointments_by_date(self, date):
        """Get all appointments for a specific date"""
        return [Appointment(**a) for a in self.appointments.values() 
                if a['appointment_date'].split('T')[0] == date]

    def get_appointments_by_patient(self, patient_id):
        """Get all appointments for a specific patient"""
        return [Appointment(**a) for a in self.appointments.values() 
                if a['patient_id'] == patient_id]

    def get_today_appointments(self):
        """Get all appointments for today"""
        today = datetime.now().strftime('%Y-%m-%d')
        return self.get_appointments_by_date(today)

    def add_medical_record(self, record):
        """Add a new medical record"""
        self.medical_records[record.id] = record.__dict__
        return record.id

    def get_medical_record(self, record_id):
        """Get medical record by ID"""
        record_data = self.medical_records.get(record_id)
        if record_data:
            return MedicalRecord(**record_data)
        return None

    def get_medical_records_by_patient(self, patient_id):
        """Get all medical records for a specific patient"""
        return [MedicalRecord(**r) for r in self.medical_records.values() 
                if r['patient_id'] == patient_id]

    def add_billing_record(self, record):
        """Add a new billing record"""
        self.billing_records[record.id] = record.__dict__
        return record.id

    def get_billing_record(self, record_id):
        """Get billing record by ID"""
        record_data = self.billing_records.get(record_id)
        if record_data:
            return BillingRecord(**record_data)
        return None

    def get_billing_records_by_patient(self, patient_id):
        """Get all billing records for a specific patient"""
        return [BillingRecord(**r) for r in self.billing_records.values() 
                if r['patient_id'] == patient_id]

    def get_department(self, department_id):
        """Get department by ID"""
        dept_data = self.departments.get(department_id)
        if dept_data:
            return Department(**dept_data)
        return None

    def get_all_departments(self):
        """Get all departments"""
        return [Department(**d) for d in self.departments.values()]

    def get_user(self, user_id):
        """Get user by ID"""
        user_data = self.users.get(user_id)
        if user_data:
            return User(**user_data)
        return None

    def get_all_users(self):
        """Get all users"""
        return [User(**u) for u in self.users.values()]

    def get_doctors(self):
        """Get all doctors"""
        return [User(**u) for u in self.users.values() if u['role'] == 'doctor']

    def log_activity(self, activity):
        """Log system activity"""
        self.activities.append(activity)
        # Keep only the last 100 activities
        if len(self.activities) > 100:
            self.activities = self.activities[-100:]

    def get_recent_activities(self, limit=10):
        """Get recent activities"""
        return sorted(self.activities, key=lambda x: x['timestamp'], reverse=True)[:limit]

    def get_inpatient_count(self):
        """Get current inpatient count"""
        return len([i for i in self.inpatients.values() if i.get('discharge_date') is None])

    def get_outpatient_count(self):
        """Get today's outpatient count"""
        today = datetime.now().strftime('%Y-%m-%d')
        return len(self.get_appointments_by_date(today))

    def get_department_visits(self, days=30):
        """Get visit statistics by department for past X days"""
        start_date = datetime.now() - timedelta(days=days)
        start_date_str = start_date.strftime('%Y-%m-%d')
        
        department_visits = {dept_id: 0 for dept_id in self.departments.keys()}
        
        for app in self.appointments.values():
            app_date = app['appointment_date'].split('T')[0]
            if app_date >= start_date_str and app['department_id'] in department_visits:
                department_visits[app['department_id']] += 1
                
        return department_visits

    def save_to_file(self):
        """Save data to JSON file for persistence"""
        try:
            data = {
                'patients': self.patients,
                'appointments': self.appointments,
                'medical_records': self.medical_records,
                'users': self.users,
                'departments': self.departments,
                'billing_records': self.billing_records,
                'pharmacy_inventory': self.pharmacy_inventory,
                'lab_requests': self.lab_requests,
                'radiology_requests': self.radiology_requests,
                'inpatients': self.inpatients,
                'activities': self.activities
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f)
            logging.info(f"Data saved to {self.data_file}")
        except Exception as e:
            logging.error(f"Error saving data: {str(e)}")

    def load_from_file(self):
        """Load data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                self.patients = data.get('patients', {})
                self.appointments = data.get('appointments', {})
                self.medical_records = data.get('medical_records', {})
                self.users = data.get('users', {})
                self.departments = data.get('departments', {})
                self.billing_records = data.get('billing_records', {})
                self.pharmacy_inventory = data.get('pharmacy_inventory', {})
                self.lab_requests = data.get('lab_requests', {})
                self.radiology_requests = data.get('radiology_requests', {})
                self.inpatients = data.get('inpatients', {})
                self.activities = data.get('activities', [])
                
                self._initialized = True
                logging.info(f"Data loaded from {self.data_file}")
            else:
                logging.info(f"No data file found at {self.data_file}, initializing with default data")
                self.initialize()
        except Exception as e:
            logging.error(f"Error loading data: {str(e)}")
            self.initialize()
