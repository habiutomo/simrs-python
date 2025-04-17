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

@main_bp.route('/billing/<bill_id>/pay-online')
def pay_billing_online(bill_id):
    """Create a Midtrans payment for a billing record"""
    from utils.midtrans import create_payment_url
    
    bill = g.data_store.get_billing_record(bill_id)
    if not bill:
        flash('Billing record not found', 'error')
        return redirect(url_for('main_bp.billing_list'))
    
    # Get the patient
    patient = g.data_store.get_patient(bill.patient_id)
    if not patient:
        flash('Patient data not found', 'error')
        return redirect(url_for('main_bp.billing_list'))
    
    try:
        # Create bill items for Midtrans
        items = []
        for item in bill.items:
            items.append({
                "id": f"{bill_id}-{item.get('id', '')}",
                "price": int(item.get('unit_price', 0)),
                "quantity": int(item.get('quantity', 1)),
                "name": item.get('description', 'Medical Service')
            })
        
        # Create Midtrans payment URL
        payment_response = create_payment_url(
            bill_id=bill_id,
            patient_name=patient.name,
            amount=bill.patient_responsibility,
            items=items,
            description=f"Medical bill payment for {patient.name}"
        )
        
        # Redirect to Midtrans payment page
        return redirect(payment_response['redirect_url'])
    except Exception as e:
        flash(f'Failed to process payment: {str(e)}', 'error')
        return redirect(url_for('main_bp.view_billing', bill_id=bill_id))

@main_bp.route('/payment/finish')
def payment_finish():
    """Handle successful payment redirect from Midtrans"""
    # Get transaction details from query parameters
    order_id = request.args.get('order_id')
    transaction_status = request.args.get('transaction_status')
    
    if transaction_status == 'settlement' or transaction_status == 'capture':
        flash('Payment successful! Thank you.', 'success')
    elif transaction_status == 'pending':
        flash('Payment is being processed. We will notify you when the payment is complete.', 'info')
    else:
        flash('Payment status: ' + transaction_status, 'info')
    
    return redirect(url_for('main_bp.billing_list'))

@main_bp.route('/payment/error')
def payment_error():
    """Handle payment error redirect from Midtrans"""
    flash('An error occurred during payment processing. Please try again.', 'error')
    return redirect(url_for('main_bp.billing_list'))

@main_bp.route('/payment/cancel')
def payment_cancel():
    """Handle payment cancellation redirect from Midtrans"""
    flash('Payment was cancelled.', 'warning')
    return redirect(url_for('main_bp.billing_list'))

@main_bp.route('/payment/notification', methods=['POST'])
def payment_notification():
    """Handle Midtrans payment notification webhook"""
    from utils.midtrans import handle_notification
    
    try:
        notification_data = request.get_json()
        result = handle_notification(notification_data)
        
        # Update billing record based on payment status
        order_id = result.get('order_id', '')
        
        # Extract the original bill_id from the order_id (if using our generated format)
        # In a real implementation, you would need to store a mapping between 
        # Midtrans order_id and your internal bill_id
        if order_id.startswith('SIMRS-BILL-'):
            parts = order_id.split('-')
            if len(parts) > 2:
                bill_id = parts[2]  # This is just an example
                
                if result['status'] == 'success':
                    # Update billing record as paid
                    bill = g.data_store.get_billing_record(bill_id)
                    if bill:
                        bill.record_payment(
                            amount=float(result.get('amount', 0)),
                            method=result.get('payment_type', 'online')
                        )
                        
                        # Update billing record in data store
                        g.data_store.billing_records[bill_id] = bill.__dict__
                        
                        # Log activity
                        patient_name = g.data_store.patients.get(bill.patient_id, {}).get('name', 'Unknown')
                        g.data_store.log_activity({
                            'timestamp': datetime.now().isoformat(),
                            'user': 'System',
                            'action': 'Online Payment Recorded',
                            'details': f"Online payment for {patient_name} via Midtrans (Order ID: {order_id})"
                        })
        
        return jsonify({'status': 'ok'})
    except Exception as e:
        current_app.logger.error(f"Payment notification error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

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
    from datetime import datetime, timedelta
    from random import randint
    
    # Sample data for demonstration
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('reports.html',
                          today_date=today_date)

@main_bp.route('/reports/create', methods=['GET', 'POST'])
def create_report():
    """Create a new report"""
    if request.method == 'POST':
        # Handle report creation
        report_name = request.form.get('reportName')
        report_category = request.form.get('reportCategory')
        report_period = request.form.get('reportPeriod')
        report_formats = request.form.getlist('reportFormat')
        
        # In a real implementation, save to database
        flash(f'Laporan "{report_name}" berhasil dibuat.', 'success')
        return redirect(url_for('main_bp.reports'))
        
    # GET request
    return render_template('create_report.html')

@main_bp.route('/reports/view/<int:report_id>')
def view_report(report_id):
    """View a specific report"""
    # In a real implementation, fetch report from database
    return render_template('view_report.html', report_id=report_id)

@main_bp.route('/reports/export/<int:report_id>')
def export_report(report_id):
    """Export a report in specified format"""
    from utils.reports import format_report_data
    
    format_type = request.args.get('format', 'pdf')
    
    # In a real implementation, generate report data
    # For now, just show a flash message
    flash(f'Laporan berhasil diekspor dalam format {format_type.upper()}.', 'success')
    return redirect(url_for('main_bp.reports'))

@main_bp.route('/reports/schedule', methods=['GET', 'POST'])
def schedule_report():
    """Schedule a report for automatic generation"""
    if request.method == 'POST':
        # Handle report scheduling
        report_id = request.form.get('reportId')
        frequency = request.form.get('scheduleFrequency')
        
        # In a real implementation, save schedule to database
        flash('Laporan berhasil dijadwalkan.', 'success')
        return redirect(url_for('main_bp.reports'))
        
    # GET request - show schedule form
    return render_template('schedule_report.html')

@main_bp.route('/analytics/dashboard')
def analytics_dashboard():
    """Display the analytics dashboard"""
    return render_template('analytics_dashboard.html')

@main_bp.route('/analytics/metrics')
def analytics_metrics():
    """Display the analytics metrics page"""
    return render_template('analytics_metrics.html')

@main_bp.route('/api/reports/data')
def api_report_data():
    """API endpoint to get report data"""
    from utils.reports import execute_report_query
    
    report_id = request.args.get('report_id')
    # In a real implementation, fetch and execute query from database
    
    return jsonify({'message': 'API for report data'})

@main_bp.route('/api/analytics/chart')
def api_analytics_chart():
    """API endpoint to get chart data for analytics"""
    chart_type = request.args.get('type', 'bar')
    period = request.args.get('period', 'monthly')
    
    # In a real implementation, fetch data and generate chart
    
    return jsonify({'message': 'API for analytics chart'})

@main_bp.route('/integration')
def integration():
    """Display the system integration page"""
    # Use data store for logs instead of direct DB query
    api_logs = g.data_store.get_recent_activities(10)
    
    return render_template('integration.html', api_logs=api_logs)

@main_bp.route('/integration/bpjs', methods=['GET', 'POST'])
def integration_bpjs():
    """Display the BPJS Kesehatan integration page"""
    from datetime import datetime
    from models.bpjs import BPJSCredential, BPJSApiLog
    
    # Check if BPJS credentials exist
    credentials = BPJSCredential.query.filter_by(is_active=True).first()
    
    # Get connection status
    connection_status = 'disconnected'
    if credentials:
        # Try to test connection (simple check if credentials exist)
        connection_status = 'connected' if all([credentials.cons_id, credentials.secret_key, credentials.user_key]) else 'disconnected'
    
    # Get service status
    service_status = {
        'peserta': connection_status == 'connected',
        'rujukan': connection_status == 'connected',
        'sep': connection_status == 'connected',
        'klaim': connection_status == 'connected',
        'aplicare': connection_status == 'connected'
    }
    
    # Get recent activity logs
    activity_logs = BPJSApiLog.query.order_by(BPJSApiLog.request_timestamp.desc()).limit(10).all()
    
    return render_template('integration_bpjs.html',
                          credentials=credentials,
                          connection_status=connection_status,
                          service_status=service_status,
                          activity_logs=activity_logs)

@main_bp.route('/integration/bpjs/update-settings', methods=['POST'])
def update_bpjs_settings():
    """Update BPJS Kesehatan API settings"""
    from models.bpjs import BPJSCredential
    from datetime import datetime
    
    if request.method == 'POST':
        # Get form data
        cons_id = request.form.get('cons_id')
        secret_key = request.form.get('secret_key')
        user_key = request.form.get('user_key')
        environment = request.form.get('environment', 'development')
        
        # Update or create credentials
        credentials = BPJSCredential.query.filter_by(is_active=True).first()
        
        if credentials:
            # Update existing credentials
            credentials.cons_id = cons_id
            credentials.secret_key = secret_key
            credentials.user_key = user_key
            credentials.environment = environment
            credentials.updated_at = datetime.now()
        else:
            # Create new credentials
            credentials = BPJSCredential(
                cons_id=cons_id,
                secret_key=secret_key,
                user_key=user_key,
                environment=environment,
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.session.add(credentials)
            
        # Save changes
        db.session.commit()
        
        flash('Pengaturan BPJS berhasil disimpan', 'success')
        
    return redirect(url_for('main_bp.integration_bpjs'))

@main_bp.route('/integration/bpjs/test-connection', methods=['POST'])
def test_bpjs_connection():
    """Test BPJS Kesehatan API connection"""
    import json
    from utils.bpjs import BPJSIntegration
    
    if request.method == 'POST':
        try:
            # Create BPJS integration instance
            bpjs = BPJSIntegration()
            
            # Test connection by checking a dummy data
            response = bpjs.check_peserta_by_noka('0000000000000')
            
            # Even if data is not found, we check if the connection was successful
            if 'metaData' in response and response['metaData']['code'] in ['200', '201']:
                return jsonify({'success': True, 'message': 'Koneksi ke API BPJS berhasil'})
            else:
                message = response.get('metaData', {}).get('message', 'Unknown error')
                return jsonify({'success': False, 'message': f'Koneksi gagal: {message}'})
                
        except Exception as e:
            return jsonify({'success': False, 'message': f'Koneksi gagal: {str(e)}'})
    
    return jsonify({'success': False, 'message': 'Invalid request method'})

@main_bp.route('/integration/bpjs/verification', methods=['GET', 'POST'])
def bpjs_verification():
    """BPJS membership verification page"""
    from datetime import datetime
    from utils.bpjs import verify_bpjs_membership
    from models.bpjs import BPJSVerificationLog
    
    verification_result = None
    search_type = 'noka'
    search_value = None
    service_date = datetime.now().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        # Get form data
        search_type = request.form.get('search_type')
        search_value = request.form.get('search_value')
        service_date = request.form.get('service_date', service_date)
        
        # Verify membership
        if search_type == 'noka':
            verification_result = verify_bpjs_membership(search_value, service_date)
        else:
            # Todo: implement NIK verification
            flash('Verifikasi menggunakan NIK belum diimplementasikan', 'warning')
            verification_result = {'validity': False, 'message': 'Verifikasi menggunakan NIK belum diimplementasikan'}
        
        # Save verification log
        if verification_result:
            log = BPJSVerificationLog(
                search_type=search_type,
                search_value=search_value,
                service_date=service_date,
                response_code=verification_result.get('raw_response', {}).get('metaData', {}).get('code'),
                response_message=verification_result.get('raw_response', {}).get('metaData', {}).get('message'),
                response_data=verification_result.get('raw_response'),
                is_valid=verification_result.get('validity', False),
                member_name=verification_result.get('nama'),
                member_status=verification_result.get('status'),
                member_nik=verification_result.get('nik'),
                member_card_number=verification_result.get('no_kartu'),
                member_class=verification_result.get('kelas'),
                member_type=verification_result.get('jenis_peserta'),
                primary_facility=verification_result.get('faskes_tingkat1'),
                created_at=datetime.now()
            )
            db.session.add(log)
            db.session.commit()
    
    # Get verification history
    verification_history = BPJSVerificationLog.query.order_by(BPJSVerificationLog.created_at.desc()).limit(10).all()
    
    return render_template('bpjs_verification.html',
                          verification_result=verification_result,
                          search_type=search_type,
                          search_value=search_value,
                          service_date=service_date,
                          verification_history=verification_history,
                          today_date=datetime.now().strftime('%Y-%m-%d'))

@main_bp.route('/integration/bpjs/referral')
def bpjs_referral():
    """BPJS referral management page"""
    return render_template('bpjs_referral.html')

@main_bp.route('/integration/bpjs/sep')
def bpjs_sep():
    """BPJS SEP management page"""
    return render_template('bpjs_sep.html')

@main_bp.route('/integration/bpjs/claim')
def bpjs_claim():
    """BPJS claim monitoring page"""
    return render_template('bpjs_claim.html')

@main_bp.route('/integration/bpjs/bed')
def bpjs_bed():
    """BPJS bed management page (Aplicare)"""
    return render_template('bpjs_bed.html')