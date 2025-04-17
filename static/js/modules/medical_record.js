/**
 * Medical Record management module for SIMRS
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize prescription form
    initPrescriptionForm();
    
    // Initialize lab results form
    initLabResultsForm();
    
    // Initialize diagnosis suggestion
    initDiagnosisSuggestion();
    
    // Initialize patient medical history
    initPatientMedicalHistory();
});

/**
 * Initialize prescription form handling
 */
function initPrescriptionForm() {
    // Add prescription item
    const addPrescriptionBtn = document.getElementById('addPrescriptionBtn');
    if (addPrescriptionBtn) {
        addPrescriptionBtn.addEventListener('click', function() {
            addPrescriptionItem();
        });
    }
    
    // Remove prescription item
    document.querySelectorAll('.remove-prescription-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const prescriptionItem = this.closest('.prescription-item');
            if (prescriptionItem) {
                prescriptionItem.remove();
            }
        });
    });
}

/**
 * Add a new prescription item to the form
 */
function addPrescriptionItem() {
    const prescriptionContainer = document.getElementById('prescriptionContainer');
    if (!prescriptionContainer) return;
    
    const index = document.querySelectorAll('.prescription-item').length;
    
    const newItem = document.createElement('div');
    newItem.className = 'prescription-item mb-3 p-3 border rounded';
    newItem.innerHTML = `
        <div class="row">
            <div class="col-md-12 d-flex justify-content-between align-items-center mb-2">
                <h6 class="mb-0">Resep #${index + 1}</h6>
                <button type="button" class="btn btn-sm btn-outline-danger remove-prescription-btn">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
        <div class="row g-2">
            <div class="col-md-6">
                <label class="form-label">Nama Obat</label>
                <input type="text" class="form-control" name="medication" required>
            </div>
            <div class="col-md-3">
                <label class="form-label">Dosis</label>
                <input type="text" class="form-control" name="dosage" placeholder="Cth: 500mg">
            </div>
            <div class="col-md-3">
                <label class="form-label">Frekuensi</label>
                <input type="text" class="form-control" name="frequency" placeholder="Cth: 3x sehari">
            </div>
        </div>
        <div class="row g-2 mt-2">
            <div class="col-md-4">
                <label class="form-label">Durasi</label>
                <input type="text" class="form-control" name="duration" placeholder="Cth: 7 hari">
            </div>
            <div class="col-md-8">
                <label class="form-label">Instruksi</label>
                <input type="text" class="form-control" name="instructions" placeholder="Cth: Setelah makan">
            </div>
        </div>
    `;
    
    prescriptionContainer.appendChild(newItem);
    
    // Add event listener to new remove button
    const removeButton = newItem.querySelector('.remove-prescription-btn');
    if (removeButton) {
        removeButton.addEventListener('click', function() {
            newItem.remove();
        });
    }
}

/**
 * Initialize lab results form handling
 */
function initLabResultsForm() {
    // Add lab result item
    const addLabResultBtn = document.getElementById('addLabResultBtn');
    if (addLabResultBtn) {
        addLabResultBtn.addEventListener('click', function() {
            addLabResultItem();
        });
    }
    
    // Remove lab result item
    document.querySelectorAll('.remove-lab-result-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const labResultItem = this.closest('.lab-result-item');
            if (labResultItem) {
                labResultItem.remove();
            }
        });
    });
}

/**
 * Add a new lab result item to the form
 */
function addLabResultItem() {
    const labResultsContainer = document.getElementById('labResultsContainer');
    if (!labResultsContainer) return;
    
    const index = document.querySelectorAll('.lab-result-item').length;
    
    const newItem = document.createElement('div');
    newItem.className = 'lab-result-item mb-3 p-3 border rounded';
    newItem.innerHTML = `
        <div class="row">
            <div class="col-md-12 d-flex justify-content-between align-items-center mb-2">
                <h6 class="mb-0">Hasil Lab #${index + 1}</h6>
                <button type="button" class="btn btn-sm btn-outline-danger remove-lab-result-btn">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
        <div class="row g-2">
            <div class="col-md-6">
                <label class="form-label">Nama Tes</label>
                <input type="text" class="form-control" name="test_name" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Hasil</label>
                <input type="text" class="form-control" name="result" required>
            </div>
        </div>
        <div class="row g-2 mt-2">
            <div class="col-md-6">
                <label class="form-label">Rentang Referensi</label>
                <input type="text" class="form-control" name="reference_range" placeholder="Cth: 70-120 mg/dL">
            </div>
            <div class="col-md-6">
                <label class="form-label">Catatan</label>
                <input type="text" class="form-control" name="notes">
            </div>
        </div>
    `;
    
    labResultsContainer.appendChild(newItem);
    
    // Add event listener to new remove button
    const removeButton = newItem.querySelector('.remove-lab-result-btn');
    if (removeButton) {
        removeButton.addEventListener('click', function() {
            newItem.remove();
        });
    }
}

/**
 * Initialize diagnosis suggestion functionality
 */
function initDiagnosisSuggestion() {
    const diagnosisInput = document.getElementById('diagnosis_input');
    const diagnosisList = document.getElementById('diagnosis_list');
    const diagnosisHidden = document.getElementById('diagnosis');
    
    if (!diagnosisInput || !diagnosisList) return;
    
    diagnosisInput.addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            addDiagnosis();
        }
    });
    
    // Add diagnosis button
    const addDiagnosisBtn = document.getElementById('addDiagnosisBtn');
    if (addDiagnosisBtn) {
        addDiagnosisBtn.addEventListener('click', function() {
            addDiagnosis();
        });
    }
}

/**
 * Add a diagnosis to the list
 */
function addDiagnosis() {
    const diagnosisInput = document.getElementById('diagnosis_input');
    const diagnosisList = document.getElementById('diagnosis_list');
    const diagnosisHidden = document.getElementById('diagnosis');
    
    if (!diagnosisInput || !diagnosisList) return;
    
    const diagnosis = diagnosisInput.value.trim();
    if (!diagnosis) return;
    
    // Create diagnosis badge
    const diagnosisItem = document.createElement('div');
    diagnosisItem.className = 'badge bg-info me-1 mb-1 p-2';
    diagnosisItem.innerHTML = `
        ${diagnosis}
        <input type="hidden" name="diagnosis" value="${diagnosis}">
        <button type="button" class="btn-close btn-close-white ms-2" style="font-size: 0.5rem;" aria-label="Remove"></button>
    `;
    
    // Add remove functionality
    const removeButton = diagnosisItem.querySelector('.btn-close');
    if (removeButton) {
        removeButton.addEventListener('click', function() {
            diagnosisItem.remove();
        });
    }
    
    diagnosisList.appendChild(diagnosisItem);
    diagnosisInput.value = '';
    diagnosisInput.focus();
}

/**
 * Initialize patient medical history display
 */
function initPatientMedicalHistory() {
    const patientSelect = document.getElementById('patient_id');
    const historyContainer = document.getElementById('medicalHistoryContainer');
    
    if (!patientSelect || !historyContainer) return;
    
    patientSelect.addEventListener('change', function() {
        const patientId = this.value;
        if (!patientId) {
            historyContainer.innerHTML = '';
            return;
        }
        
        // In a real application, fetch patient medical history from API
        // For now, just show a loading indicator
        historyContainer.innerHTML = '<p class="text-center"><i class="fas fa-spinner fa-spin"></i> Memuat riwayat medis...</p>';
        
        // Simulate API call
        setTimeout(function() {
            // This would be replaced with actual API data
            historyContainer.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Riwayat medis pasien akan ditampilkan di sini (data contoh).
                </div>
                <div class="card mb-3">
                    <div class="card-header">
                        <h6>Riwayat Kunjungan Terakhir</h6>
                    </div>
                    <div class="card-body">
                        <p><small>Belum ada riwayat kunjungan untuk pasien ini.</small></p>
                    </div>
                </div>
            `;
        }, 1000);
    });
}
