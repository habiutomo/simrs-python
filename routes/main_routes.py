from flask import Blueprint, render_template, request, redirect, url_for, g, flash, jsonify, session
from datetime import datetime, timedelta
import uuid
import json

from models.patient import Patient
from models.appointment import Appointment
from models.medical_record import MedicalRecord
from models.billing import BillingRecord

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    """Main entry point, redirects to dashboard"""
    return redirect(url_for('main_bp.dashboard'))

@main_bp.route('/dashboard')
def dashboard():
    """Display the dashboard with hospital statistics"""
    data_store = g.data_store
    
    # Get statistics for dashboard
    total_patients = len(data_store.patients)
    appointments_today = len(data_store.get_today_appointments())
    inpatient_count = data_store.get_inpatient_count()
    doctors_on_duty = len([u for u in data_store.users.values() if u.get('role') == 'doctor'])
    
    # Get department visit statistics
    department_visits = data_store.get_department_visits(30)
    departments = {d_id: d.get('name') for d_id, d in data_store.departments.items()}
    
    # Get recent activities
    activities = data_store.get_recent_activities(5)
    
    return render_template('dashboard.html', 
                           total_patients=total_patients,
                           appointments_today=appointments_today,
                           inpatient_count=inpatient_count,
                           doctors_on_duty=doctors_on_duty,
                           department_visits=department_visits,
                           departments=departments,
                           activities=activities)

@main_bp.route('/patient')
def patient_list():
    """Display the patient list page"""
    patients = g.data_store.get_all_patients()
    return render_template('patient.html', patients=patients)

@main_bp.route('/patient/add', methods=['GET', 'POST'])
def add_patient():
    """Add a new patient"""
    if request.method == 'POST':
        # Extract patient data from form
        new_patient = Patient(
            name=request.form.get('name'),
            gender=request.form.get('gender'),
            birth_date=request.form.get('birth_date'),
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            id_number=request.form.get('id_number'),
            insurance_number=request.form.get('insurance_number'),
            insurance_provider=request.form.get('insurance_provider'),
            blood_type=request.form.get('blood_type'),
            allergies=request.form.get('allergies', '').split(',') if request.form.get('allergies') else [],
            emergency_contact={
                'name': request.form.get('emergency_name'),
                'phone': request.form.get('emergency_phone'),
                'relationship': request.form.get('emergency_relationship')
            }
        )
        
        # Save patient to data store
        g.data_store.add_patient(new_patient)
        
        # Log activity
        g.data_store.log_activity({
            'timestamp': datetime.now().isoformat(),
            'user': 'System',
            'action': 'Patient Registration',
            'details': f"New patient registered: {new_patient.name}"
        })
        
        flash('Patient added successfully', 'success')
        return redirect(url_for('main_bp.patient_list'))
    
    return render_template('patient.html', action="add")

@main_bp.route('/patient/<patient_id>')
def view_patient(patient_id):
    """View patient details"""
    patient = g.data_store.get_patient(patient_id)
    if not patient:
        flash('Patient not found', 'error')
        return redirect(url_for('main_bp.patient_list'))
    
    medical_records = g.data_store.get_medical_records_by_patient(patient_id)
    appointments = g.data_store.get_appointments_by_patient(patient_id)
    billing_records = g.data_store.get_billing_records_by_patient(patient_id)
    
    return render_template('patient.html', 
                          patient=patient, 
                          medical_records=medical_records,
                          appointments=appointments,
                          billing_records=billing_records,
                          action="view")

@main_bp.route('/appointment')
def appointment_list():
    """Display the appointment list page"""
    # Get date filter from query params, default to today
    date_filter = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    if date_filter == 'today':
        date_filter = datetime.now().strftime('%Y-%m-%d')
    elif date_filter == 'tomorrow':
        tomorrow = datetime.now() + timedelta(days=1)
        date_filter = tomorrow.strftime('%Y-%m-%d')
    elif date_filter == 'week':
        # Show appointments for the next 7 days
        start_date = datetime.now()
        end_date = start_date + timedelta(days=7)
        appointments = []
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            daily_appointments = g.data_store.get_appointments_by_date(date_str)
            appointments.extend(daily_appointments)
            current_date += timedelta(days=1)
    else:
        # Show appointments for specific date
        appointments = g.data_store.get_appointments_by_date(date_filter)
    
    # If not showing for a week, get appointments for the specific date
    if date_filter != 'week':
        appointments = g.data_store.get_appointments_by_date(date_filter)
    
    # Get patient and doctor information for displaying in the list
    patients = {p_id: p.get('name') for p_id, p in g.data_store.patients.items()}
    doctors = {d_id: d.get('name') for d_id, d in g.data_store.users.items() 
               if d.get('role') == 'doctor'}
    departments = {d_id: d.get('name') for d_id, d in g.data_store.departments.items()}
    
    return render_template('appointment.html', 
                           appointments=appointments,
                           patients=patients,
                           doctors=doctors,
                           departments=departments,
                           date_filter=date_filter)

@main_bp.route('/appointment/add', methods=['GET', 'POST'])
def add_appointment():
    """Add a new appointment"""
    if request.method == 'POST':
        # Extract appointment data from form
        new_appointment = Appointment(
            patient_id=request.form.get('patient_id'),
            doctor_id=request.form.get('doctor_id'),
            department_id=request.form.get('department_id'),
            appointment_date=request.form.get('appointment_date'),
            appointment_time=request.form.get('appointment_time'),
            reason=request.form.get('reason'),
            notes=request.form.get('notes')
        )
        
        # Save appointment to data store
        g.data_store.add_appointment(new_appointment)
        
        # Log activity
        patient_name = g.data_store.patients.get(new_appointment.patient_id, {}).get('name', 'Unknown')
        g.data_store.log_activity({
            'timestamp': datetime.now().isoformat(),
            'user': 'System',
            'action': 'Appointment Scheduled',
            'details': f"New appointment for {patient_name} on {new_appointment.appointment_date}"
        })
        
        flash('Appointment added successfully', 'success')
        return redirect(url_for('main_bp.appointment_list'))
    
    # Get patients and doctors for dropdown lists
    patients = g.data_store.get_all_patients()
    doctors = g.data_store.get_doctors()
    departments = g.data_store.get_all_departments()
    
    return render_template('appointment.html', 
                          action="add",
                          patients=patients,
                          doctors=doctors,
                          departments=departments)

@main_bp.route('/medical-record')
def medical_record_list():
    """Display the medical records list page"""
    records = []
    for record_id, record in g.data_store.medical_records.items():
        patient_id = record.get('patient_id')
        patient_name = g.data_store.patients.get(patient_id, {}).get('name', 'Unknown')
        doctor_id = record.get('doctor_id')
        doctor_name = g.data_store.users.get(doctor_id, {}).get('name', 'Unknown')
        
        records.append({
            'id': record_id,
            'patient_name': patient_name,
            'doctor_name': doctor_name,
            'visit_date': record.get('visit_date'),
            'diagnosis': record.get('diagnosis'),
            'record_type': record.get('record_type')
        })
    
    return render_template('medical_record.html', records=records)

@main_bp.route('/medical-record/add', methods=['GET', 'POST'])
def add_medical_record():
    """Add a new medical record"""
    if request.method == 'POST':
        # Extract medical record data from form
        new_record = MedicalRecord(
            patient_id=request.form.get('patient_id'),
            doctor_id=request.form.get('doctor_id'),
            visit_date=request.form.get('visit_date') or datetime.now().isoformat(),
            chief_complaint=request.form.get('chief_complaint'),
            diagnosis=request.form.getlist('diagnosis'),
            treatment=request.form.get('treatment'),
            notes=request.form.get('notes'),
            record_type=request.form.get('record_type')
        )
        
        # Extract and add vitals
        if request.form.get('blood_pressure') or request.form.get('heart_rate') or \
           request.form.get('temperature') or request.form.get('respiratory_rate') or \
           request.form.get('oxygen_saturation'):
            new_record.update_vitals(
                blood_pressure=request.form.get('blood_pressure'),
                heart_rate=request.form.get('heart_rate'),
                temperature=request.form.get('temperature'),
                respiratory_rate=request.form.get('respiratory_rate'),
                oxygen_saturation=request.form.get('oxygen_saturation'),
                height=request.form.get('height'),
                weight=request.form.get('weight')
            )
        
        # Extract and add prescriptions
        if request.form.getlist('medication'):
            medications = request.form.getlist('medication')
            dosages = request.form.getlist('dosage')
            frequencies = request.form.getlist('frequency')
            durations = request.form.getlist('duration')
            instructions = request.form.getlist('instructions')
            
            for i in range(len(medications)):
                if medications[i]:
                    new_record.add_prescription(
                        medication=medications[i],
                        dosage=dosages[i] if i < len(dosages) else "",
                        frequency=frequencies[i] if i < len(frequencies) else "",
                        duration=durations[i] if i < len(durations) else "",
                        instructions=instructions[i] if i < len(instructions) else ""
                    )
        
        # Save medical record to data store
        g.data_store.add_medical_record(new_record)
        
        # Log activity
        patient_name = g.data_store.patients.get(new_record.patient_id, {}).get('name', 'Unknown')
        g.data_store.log_activity({
            'timestamp': datetime.now().isoformat(),
            'user': 'System',
            'action': 'Medical Record Created',
            'details': f"New medical record for {patient_name} created"
        })
        
        flash('Medical record added successfully', 'success')
        return redirect(url_for('main_bp.medical_record_list'))
    
    # Get patients and doctors for dropdown lists
    patients = g.data_store.get_all_patients()
    doctors = g.data_store.get_doctors()
    
    return render_template('medical_record.html', 
                          action="add",
                          patients=patients,
                          doctors=doctors)

@main_bp.route('/medical-record/<record_id>')
def view_medical_record(record_id):
    """View medical record details"""
    record = g.data_store.get_medical_record(record_id)
    if not record:
        flash('Medical record not found', 'error')
        return redirect(url_for('main_bp.medical_record_list'))
    
    patient = g.data_store.get_patient(record.patient_id)
    doctor = g.data_store.get_user(record.doctor_id)
    
    return render_template('medical_record.html', 
                          record=record, 
                          patient=patient,
                          doctor=doctor,
                          action="view")

@main_bp.route('/inpatient')
def inpatient_list():
    """Display the inpatient list page"""
    inpatients = []
    for patient_id, inpatient in g.data_store.inpatients.items():
        if not inpatient.get('discharge_date'):  # Only show active inpatients
            patient = g.data_store.patients.get(patient_id, {})
            inpatients.append({
                'id': patient_id,
                'name': patient.get('name', 'Unknown'),
                'admission_date': inpatient.get('admission_date'),
                'diagnosis': inpatient.get('primary_diagnosis'),
                'room': inpatient.get('room'),
                'doctor': g.data_store.users.get(inpatient.get('attending_doctor_id'), {}).get('name', 'Unknown')
            })
    
    return render_template('inpatient.html', inpatients=inpatients)

@main_bp.route('/pharmacy')
def pharmacy():
    """Display the pharmacy page"""
    # Get prescriptions from medical records
    prescriptions = []
    for record_id, record in g.data_store.medical_records.items():
        for prescription in record.get('prescriptions', []):
            patient_id = record.get('patient_id')
            patient_name = g.data_store.patients.get(patient_id, {}).get('name', 'Unknown')
            
            prescriptions.append({
                'record_id': record_id,
                'patient_id': patient_id,
                'patient_name': patient_name,
                'medication': prescription.get('medication'),
                'dosage': prescription.get('dosage'),
                'frequency': prescription.get('frequency'),
                'duration': prescription.get('duration'),
                'instructions': prescription.get('instructions'),
                'prescribed_at': prescription.get('prescribed_at')
            })
    
    # Get pharmacy inventory
    inventory = g.data_store.pharmacy_inventory
    
    return render_template('pharmacy.html', 
                          prescriptions=prescriptions,
                          inventory=inventory)

@main_bp.route('/laboratory')
def laboratory():
    """Display the laboratory page"""
    # Get lab requests
    lab_requests = g.data_store.lab_requests
    
    # Get completed lab results from medical records
    lab_results = []
    for record_id, record in g.data_store.medical_records.items():
        for result in record.get('lab_results', []):
            patient_id = record.get('patient_id')
            patient_name = g.data_store.patients.get(patient_id, {}).get('name', 'Unknown')
            
            lab_results.append({
                'record_id': record_id,
                'patient_id': patient_id,
                'patient_name': patient_name,
                'test_name': result.get('test_name'),
                'result': result.get('result'),
                'reference_range': result.get('reference_range'),
                'notes': result.get('notes'),
                'recorded_at': result.get('recorded_at')
            })
    
    return render_template('laboratory.html', 
                          lab_requests=lab_requests,
                          lab_results=lab_results)

@main_bp.route('/radiology')
def radiology():
    """Display the radiology page"""
    # Get radiology requests
    radiology_requests = g.data_store.radiology_requests
    
    return render_template('radiology.html', 
                          radiology_requests=radiology_requests)
                          
@main_bp.route('/physiotherapy')
def physiotherapy():
    """Display the physiotherapy page"""
    # Get physiotherapy appointments/sessions
    physiotherapy_sessions = []
    
    # In a real application, these would come from the database
    # For now, we'll create sample data for display purposes
    today = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('physiotherapy.html', 
                          physiotherapy_sessions=physiotherapy_sessions,
                          today=today)

@main_bp.route('/billing')
def billing_list():
    """Display the billing list page"""
    bills = []
    for bill_id, bill in g.data_store.billing_records.items():
        patient_id = bill.get('patient_id')
        patient_name = g.data_store.patients.get(patient_id, {}).get('name', 'Unknown')
        
        bills.append({
            'id': bill_id,
            'patient_id': patient_id,
            'patient_name': patient_name,
            'total_amount': bill.get('total_amount'),
            'patient_responsibility': bill.get('patient_responsibility'),
            'status': bill.get('status'),
            'issued_date': bill.get('issued_date'),
            'due_date': bill.get('due_date')
        })
    
    return render_template('billing.html', bills=bills)

@main_bp.route('/billing/add', methods=['GET', 'POST'])
def add_billing():
    """Add a new billing record"""
    if request.method == 'POST':
        # Extract billing data from form
        items = []
        descriptions = request.form.getlist('description')
        quantities = request.form.getlist('quantity')
        unit_prices = request.form.getlist('unit_price')
        item_types = request.form.getlist('item_type')
        
        for i in range(len(descriptions)):
            if descriptions[i] and quantities[i] and unit_prices[i]:
                items.append({
                    'description': descriptions[i],
                    'quantity': int(quantities[i]),
                    'unit_price': float(unit_prices[i]),
                    'total': int(quantities[i]) * float(unit_prices[i]),
                    'item_type': item_types[i] if i < len(item_types) else 'service'
                })
        
        # Calculate totals
        total_amount = sum(item['total'] for item in items)
        insurance_covered = float(request.form.get('insurance_covered', 0))
        patient_responsibility = max(0, total_amount - insurance_covered)
        
        # Due date is 30 days from issued date
        issued_date = request.form.get('issued_date') or datetime.now().isoformat()
        due_date_obj = datetime.fromisoformat(issued_date.replace('Z', '+00:00')) + timedelta(days=30)
        due_date = due_date_obj.isoformat()
        
        new_bill = BillingRecord(
            patient_id=request.form.get('patient_id'),
            visit_id=request.form.get('visit_id'),
            visit_type=request.form.get('visit_type'),
            items=items,
            total_amount=total_amount,
            insurance_covered=insurance_covered,
            patient_responsibility=patient_responsibility,
            issued_date=issued_date,
            due_date=due_date,
            notes=request.form.get('notes')
        )
        
        # Save billing record to data store
        g.data_store.add_billing_record(new_bill)
        
        # Log activity
        patient_name = g.data_store.patients.get(new_bill.patient_id, {}).get('name', 'Unknown')
        g.data_store.log_activity({
            'timestamp': datetime.now().isoformat(),
            'user': 'System',
            'action': 'Billing Record Created',
            'details': f"New billing record for {patient_name} created (Amount: {total_amount})"
        })
        
        flash('Billing record added successfully', 'success')
        return redirect(url_for('main_bp.billing_list'))
    
    # Get patients for dropdown list
    patients = g.data_store.get_all_patients()
    
    # Get appointments and medical records for visit selection
    appointments = []
    for app_id, app in g.data_store.appointments.items():
        patient_id = app.get('patient_id')
        patient_name = g.data_store.patients.get(patient_id, {}).get('name', 'Unknown')
        
        appointments.append({
            'id': app_id,
            'patient_id': patient_id,
            'patient_name': patient_name,
            'appointment_date': app.get('appointment_date'),
            'visit_type': 'outpatient'
        })
    
    return render_template('billing.html', 
                          action="add",
                          patients=patients,
                          appointments=appointments)

@main_bp.route('/billing/<bill_id>')
def view_billing(bill_id):
    """View billing record details"""
    bill = g.data_store.get_billing_record(bill_id)
    if not bill:
        flash('Billing record not found', 'error')
        return redirect(url_for('main_bp.billing_list'))
    
    patient = g.data_store.get_patient(bill.patient_id)
    
    return render_template('billing.html', 
                          bill=bill, 
                          patient=patient,
                          action="view")

@main_bp.route('/billing/<bill_id>/pay', methods=['GET', 'POST'])
def pay_billing(bill_id):
    """Record payment for a billing record"""
    bill = g.data_store.get_billing_record(bill_id)
    if not bill:
        flash('Billing record not found', 'error')
        return redirect(url_for('main_bp.billing_list'))
    
    # GET request will show the payment form
    if request.method == 'GET':
        patient = g.data_store.get_patient(bill.patient_id)
        return render_template('billing.html', 
                              bill=bill, 
                              patient=patient,
                              action="pay")
    
    # POST request will process the payment
    amount = float(request.form.get('amount', 0))
    method = request.form.get('payment_method', 'cash')
    
    bill.record_payment(amount, method)
    
    # Update billing record in data store
    g.data_store.billing_records[bill_id] = bill.__dict__
    
    # Log activity
    patient_name = g.data_store.patients.get(bill.patient_id, {}).get('name', 'Unknown')
    g.data_store.log_activity({
        'timestamp': datetime.now().isoformat(),
        'user': 'System',
        'action': 'Payment Recorded',
        'details': f"Payment of {amount} recorded for {patient_name} (Method: {method})"
    })
    
    flash('Payment recorded successfully', 'success')
    return redirect(url_for('main_bp.view_billing', bill_id=bill_id))

@main_bp.route('/department')
def department_stats():
    """Display department statistics page"""
    # Get department visit statistics
    department_visits = g.data_store.get_department_visits(30)
    departments = g.data_store.get_all_departments()
    
    return render_template('department.html', 
                          department_visits=department_visits,
                          departments=departments)

@main_bp.route('/settings')
def settings():
    """Display settings page"""
    return render_template('settings.html')

@main_bp.route('/settings/language', methods=['POST'])
def set_language():
    """Set application language"""
    locale = request.form.get('locale', 'id')
    session['locale'] = locale
    return redirect(url_for('main_bp.settings'))

# Administrative Module Routes

@main_bp.route('/accounting')
def accounting():
    """Display the accounting page"""
    return render_template('accounting.html')

@main_bp.route('/procurement')
def procurement():
    """Display the procurement page"""
    return render_template('procurement.html')

@main_bp.route('/inventory')
def inventory():
    """Display the inventory and assets page"""
    return render_template('inventory.html')

@main_bp.route('/human-resources')
def human_resources():
    """Display the human resources page"""
    return render_template('hr.html')

@main_bp.route('/payroll')
def payroll():
    """Display the payroll page"""
    return render_template('payroll.html')

@main_bp.route('/reports')
def reports():
    """Display the reports and analytics page"""
    return render_template('reports.html')

@main_bp.route('/integration')
def integration():
    """Display the system integration page"""
    return render_template('integration.html')
