/**
 * Inpatient management module for SIMRS
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize inpatient search
    initInpatientSearch();
    
    // Initialize bed assignment
    initBedAssignment();
    
    // Initialize inpatient status update
    initStatusUpdate();
});

/**
 * Initialize inpatient search functionality
 */
function initInpatientSearch() {
    const searchInput = document.getElementById('searchInpatient');
    if (!searchInput) return;
    
    searchInput.addEventListener('keyup', function() {
        const searchText = this.value.toLowerCase();
        const inpatientTable = document.getElementById('inpatientTable');
        if (!inpatientTable) return;
        
        const rows = inpatientTable.querySelectorAll('tbody tr');
        
        rows.forEach(function(row) {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchText) ? '' : 'none';
        });
    });
}

/**
 * Initialize bed assignment functionality
 */
function initBedAssignment() {
    const roomSelect = document.getElementById('room_id');
    const bedSelect = document.getElementById('bed_id');
    
    if (!roomSelect || !bedSelect) return;
    
    roomSelect.addEventListener('change', function() {
        const roomId = this.value;
        
        // Reset bed select
        bedSelect.innerHTML = '<option value="">Pilih tempat tidur...</option>';
        
        if (!roomId) return;
        
        // In a real application, this would fetch available beds for the selected room
        // For now, simulate loading
        bedSelect.disabled = true;
        
        setTimeout(function() {
            // Re-enable the select
            bedSelect.disabled = false;
            
            // Simulate adding beds (would come from API in real app)
            const beds = [
                { id: 'A1', name: 'Bed A1' },
                { id: 'A2', name: 'Bed A2' },
                { id: 'A3', name: 'Bed A3' },
                { id: 'A4', name: 'Bed A4' }
            ];
            
            beds.forEach(function(bed) {
                const option = document.createElement('option');
                option.value = bed.id;
                option.textContent = bed.name;
                bedSelect.appendChild(option);
            });
        }, 500);
    });
}

/**
 * Initialize inpatient status update functionality
 */
function initStatusUpdate() {
    // Discharge patient
    document.querySelectorAll('.discharge-patient-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const patientId = this.getAttribute('data-id');
            if (confirm('Apakah Anda yakin ingin mengeluarkan pasien ini dari rawat inap?')) {
                dischargePatient(patientId);
            }
        });
    });
    
    // Transfer patient
    document.querySelectorAll('.transfer-patient-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const patientId = this.getAttribute('data-id');
            showTransferModal(patientId);
        });
    });
}

/**
 * Discharge a patient
 * @param {string} patientId - Patient ID
 */
function dischargePatient(patientId) {
    // In a real application, this would be an API call
    // For now, just show an alert and reload
    alert('Pasien akan dikeluarkan dari rawat inap');
    window.location.reload();
}

/**
 * Show transfer modal for a patient
 * @param {string} patientId - Patient ID
 */
function showTransferModal(patientId) {
    // Get the transfer modal
    const transferModal = document.getElementById('transferModal');
    if (!transferModal) return;
    
    // Set patient ID in the form
    const patientIdInput = transferModal.querySelector('input[name="patient_id"]');
    if (patientIdInput) {
        patientIdInput.value = patientId;
    }
    
    // Show the modal
    const modal = new bootstrap.Modal(transferModal);
    modal.show();
}

/**
 * Add daily note for an inpatient
 * @param {string} patientId - Patient ID
 */
function addDailyNote(patientId) {
    // Get the daily note modal
    const noteModal = document.getElementById('dailyNoteModal');
    if (!noteModal) return;
    
    // Set patient ID in the form
    const patientIdInput = noteModal.querySelector('input[name="patient_id"]');
    if (patientIdInput) {
        patientIdInput.value = patientId;
    }
    
    // Show the modal
    const modal = new bootstrap.Modal(noteModal);
    modal.show();
}

/**
 * Update vitals for an inpatient
 * @param {string} patientId - Patient ID
 */
function updateVitals(patientId) {
    // Get the vitals modal
    const vitalsModal = document.getElementById('vitalsModal');
    if (!vitalsModal) return;
    
    // Set patient ID in the form
    const patientIdInput = vitalsModal.querySelector('input[name="patient_id"]');
    if (patientIdInput) {
        patientIdInput.value = patientId;
    }
    
    // Show the modal
    const modal = new bootstrap.Modal(vitalsModal);
    modal.show();
}
