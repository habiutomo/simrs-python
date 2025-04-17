from flask import Blueprint, request, jsonify, g
from datetime import datetime
import uuid
import json

from models.patient import Patient
from models.appointment import Appointment
from models.medical_record import MedicalRecord
from models.billing import BillingRecord

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/patients', methods=['GET'])
def get_patients():
    """API endpoint to get all patients"""
    patients = g.data_store.get_all_patients()
    return jsonify([p.__dict__ for p in patients])

@api_bp.route('/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    """API endpoint to get a specific patient"""
    patient = g.data_store.get_patient(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    return jsonify(patient.__dict__)

@api_bp.route('/appointments', methods=['GET'])
def get_appointments():
    """API endpoint to get appointments"""
    date = request.args.get('date')
    if date:
        appointments = g.data_store.get_appointments_by_date(date)
    else:
        appointments = [Appointment(**a) for a in g.data_store.appointments.values()]
    return jsonify([a.__dict__ for a in appointments])

@api_bp.route('/appointments/<appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """API endpoint to get a specific appointment"""
    appointment = g.data_store.get_appointment(appointment_id)
    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404
    return jsonify(appointment.__dict__)

@api_bp.route('/medical-records', methods=['GET'])
def get_medical_records():
    """API endpoint to get medical records"""
    patient_id = request.args.get('patient_id')
    if patient_id:
        records = g.data_store.get_medical_records_by_patient(patient_id)
    else:
        records = [MedicalRecord(**r) for r in g.data_store.medical_records.values()]
    return jsonify([r.__dict__ for r in records])

@api_bp.route('/medical-records/<record_id>', methods=['GET'])
def get_medical_record(record_id):
    """API endpoint to get a specific medical record"""
    record = g.data_store.get_medical_record(record_id)
    if not record:
        return jsonify({'error': 'Medical record not found'}), 404
    return jsonify(record.__dict__)

@api_bp.route('/dashboard/statistics', methods=['GET'])
def get_dashboard_statistics():
    """API endpoint to get dashboard statistics"""
    data_store = g.data_store
    
    # Get statistics for dashboard
    total_patients = len(data_store.patients)
    appointments_today = len(data_store.get_today_appointments())
    inpatient_count = data_store.get_inpatient_count()
    doctors_on_duty = len([u for u in data_store.users.values() if u.get('role') == 'doctor'])
    
    # Get department visit statistics
    department_visits = data_store.get_department_visits(30)
    departments = {d_id: d.get('name') for d_id, d in data_store.departments.items()}
    
    # Format department statistics for chart
    department_stats = []
    for dept_id, visits in department_visits.items():
        if dept_id in departments:
            department_stats.append({
                'department': departments[dept_id],
                'visits': visits
            })
    
    return jsonify({
        'total_patients': total_patients,
        'appointments_today': appointments_today,
        'inpatient_count': inpatient_count,
        'doctors_on_duty': doctors_on_duty,
        'department_visits': department_stats
    })

@api_bp.route('/bpjs/verify', methods=['GET'])
def verify_bpjs():
    """Mock BPJS verification endpoint"""
    insurance_number = request.args.get('insurance_number')
    
    # Mock verification - in a real system, this would call the BPJS API
    if insurance_number and len(insurance_number) >= 8:
        return jsonify({
            'status': 'active',
            'member_name': 'Mock BPJS Member',
            'validity': 'Valid',
            'class': '1'
        })
    else:
        return jsonify({
            'status': 'inactive',
            'error': 'Invalid insurance number'
        }), 400

@api_bp.route('/activities', methods=['GET'])
def get_activities():
    """API endpoint to get recent activities"""
    limit = int(request.args.get('limit', 10))
    activities = g.data_store.get_recent_activities(limit)
    return jsonify(activities)
