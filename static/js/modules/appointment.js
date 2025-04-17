/**
 * Appointment management module for SIMRS
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize appointment search
    initAppointmentSearch();
    
    // Initialize appointment date filter
    initDateFilter();
    
    // Initialize department-doctor filter
    initDepartmentDoctorFilter();
    
    // Initialize appointment status update
    initStatusUpdate();
});

/**
 * Initialize appointment search functionality
 */
function initAppointmentSearch() {
    const searchInput = document.getElementById('searchAppointment');
    if (!searchInput) return;
    
    searchInput.addEventListener('keyup', function() {
        const searchText = this.value.toLowerCase();
        const appointmentTable = document.getElementById('appointmentTable');
        if (!appointmentTable) return;
        
        const rows = appointmentTable.querySelectorAll('tbody tr');
        
        rows.forEach(function(row) {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchText) ? '' : 'none';
        });
    });
}

/**
 * Initialize appointment date filter
 */
function initDateFilter() {
    const filterDateInput = document.getElementById('filterDate');
    const applyDateFilter = document.getElementById('applyDateFilter');
    
    if (!filterDateInput || !applyDateFilter) return;
    
    applyDateFilter.addEventListener('click', function() {
        const date = filterDateInput.value;
        if (date) {
            window.location.href = `/appointment?date=${date}`;
        }
    });
    
    // Allow pressing Enter to apply filter
    filterDateInput.addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            applyDateFilter.click();
        }
    });
}

/**
 * Initialize department-doctor filter relationship
 */
function initDepartmentDoctorFilter() {
    const departmentSelect = document.getElementById('department_id');
    const doctorSelect = document.getElementById('doctor_id');
    
    if (!departmentSelect || !doctorSelect) return;
    
    departmentSelect.addEventListener('change', function() {
        const departmentId = this.value;
        
        // Reset doctor select
        doctorSelect.innerHTML = '<option value="">Pilih dokter...</option>';
        
        if (!departmentId) return;
        
        // Simulate loading doctors by department
        // In a real application, this would fetch from the server
        doctorSelect.disabled = true;
        
        setTimeout(function() {
            // This would normally be an API call
            // For now, let's use the existing options but filter them
            const doctorOptions = Array.from(document.querySelectorAll('select[id="doctor_id"] option'));
            
            // Re-enable the select
            doctorSelect.disabled = false;
            
            // In a real application, filter doctors by department
            // For now, just re-add all doctors (would be filtered in production)
            doctorOptions.forEach(option => {
                if (option.value) {
                    doctorSelect.appendChild(option.cloneNode(true));
                }
            });
        }, 500);
    });
}

/**
 * Initialize appointment status update buttons
 */
function initStatusUpdate() {
    // Complete appointment
    document.querySelectorAll('.complete-appointment-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const appointmentId = this.getAttribute('data-id');
            updateAppointmentStatus(appointmentId, 'completed');
        });
    });
    
    // Cancel appointment
    document.querySelectorAll('.cancel-appointment-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const appointmentId = this.getAttribute('data-id');
            if (confirm('Apakah Anda yakin ingin membatalkan janji temu ini?')) {
                updateAppointmentStatus(appointmentId, 'cancelled');
            }
        });
    });
    
    // Mark as no-show
    document.querySelectorAll('.no-show-appointment-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const appointmentId = this.getAttribute('data-id');
            if (confirm('Tandai pasien tidak hadir pada janji temu ini?')) {
                updateAppointmentStatus(appointmentId, 'no-show');
            }
        });
    });
}

/**
 * Update appointment status
 * @param {string} appointmentId - Appointment ID
 * @param {string} status - New status (completed, cancelled, no-show)
 */
function updateAppointmentStatus(appointmentId, status) {
    // In a real application, this would be an API call
    // For now, just reload the page
    alert(`Status janji temu akan diubah menjadi ${status}`);
    window.location.reload();
}

/**
 * Start examination for an appointment
 * @param {string} appointmentId - Appointment ID
 * @param {string} patientId - Patient ID
 */
function startExamination(appointmentId, patientId) {
    // Redirect to add medical record page with appointment info
    window.location.href = `/medical-record/add?patient_id=${patientId}&appointment_id=${appointmentId}`;
}

/**
 * Check available time slots for the selected date
 */
function checkAvailableTimeSlots() {
    const dateInput = document.getElementById('appointment_date');
    const timeInput = document.getElementById('appointment_time');
    const doctorSelect = document.getElementById('doctor_id');
    
    if (!dateInput || !timeInput || !doctorSelect) return;
    
    const selectedDate = dateInput.value;
    const selectedDoctor = doctorSelect.value;
    
    if (!selectedDate || !selectedDoctor) return;
    
    // In a real application, this would be an API call to check available time slots
    // For now, just simulate loading
    timeInput.disabled = true;
    
    setTimeout(function() {
        // Re-enable the time input
        timeInput.disabled = false;
        
        // This would normally show available time slots based on API response
        // For now, just show a message
        const timeSlotMessage = document.getElementById('timeSlotMessage');
        if (timeSlotMessage) {
            timeSlotMessage.innerHTML = '<small class="text-success">Jam yang dipilih tersedia</small>';
        }
    }, 1000);
}
