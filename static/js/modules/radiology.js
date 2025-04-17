/**
 * Radiology management module for SIMRS
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize radiology request search
    initRadiologyRequestSearch();
    
    // Initialize radiology modalities
    initRadiologyModalities();
    
    // Initialize radiology result entry
    initRadiologyResultEntry();
});

/**
 * Initialize radiology request search functionality
 */
function initRadiologyRequestSearch() {
    const searchInput = document.getElementById('searchRadiologyRequest');
    if (!searchInput) return;
    
    searchInput.addEventListener('keyup', function() {
        const searchText = this.value.toLowerCase();
        const radiologyRequestTable = document.getElementById('radiologyRequestTable');
        if (!radiologyRequestTable) return;
        
        const rows = radiologyRequestTable.querySelectorAll('tbody tr');
        
        rows.forEach(function(row) {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchText) ? '' : 'none';
        });
    });
}

/**
 * Initialize radiology modalities functionality
 */
function initRadiologyModalities() {
    const modalitySelect = document.getElementById('modalityType');
    const examSelect = document.getElementById('examName');
    
    if (!modalitySelect || !examSelect) return;
    
    modalitySelect.addEventListener('change', function() {
        const modality = this.value;
        
        // Reset exam select
        examSelect.innerHTML = '<option value="">Pilih pemeriksaan...</option>';
        
        if (!modality) return;
        
        // In a real application, this would fetch exams for the selected modality
        // For now, simulate loading
        examSelect.disabled = true;
        
        setTimeout(function() {
            // Re-enable the select
            examSelect.disabled = false;
            
            // Add sample exams based on modality (would come from API in real app)
            let exams = [];
            
            if (modality === 'x-ray') {
                exams = [
                    { id: 'xr1', name: 'Chest X-Ray' },
                    { id: 'xr2', name: 'Abdominal X-Ray' },
                    { id: 'xr3', name: 'Skull X-Ray' },
                    { id: 'xr4', name: 'Spine X-Ray' }
                ];
            } else if (modality === 'ct-scan') {
                exams = [
                    { id: 'ct1', name: 'CT Scan Kepala' },
                    { id: 'ct2', name: 'CT Scan Thorax' },
                    { id: 'ct3', name: 'CT Scan Abdomen' },
                    { id: 'ct4', name: 'CT Scan Spine' }
                ];
            } else if (modality === 'mri') {
                exams = [
                    { id: 'mri1', name: 'MRI Kepala' },
                    { id: 'mri2', name: 'MRI Spine' },
                    { id: 'mri3', name: 'MRI Abdomen' },
                    { id: 'mri4', name: 'MRI Ekstremitas' }
                ];
            } else if (modality === 'usg') {
                exams = [
                    { id: 'usg1', name: 'USG Abdomen' },
                    { id: 'usg2', name: 'USG Obstetri' },
                    { id: 'usg3', name: 'USG Thyroid' },
                    { id: 'usg4', name: 'USG Mammae' }
                ];
            }
            
            exams.forEach(function(exam) {
                const option = document.createElement('option');
                option.value = exam.id;
                option.textContent = exam.name;
                examSelect.appendChild(option);
            });
        }, 500);
    });
}

/**
 * Initialize radiology result entry functionality
 */
function initRadiologyResultEntry() {
    // Process radiology request button
    document.querySelectorAll('.process-radiology-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const requestId = this.getAttribute('data-id');
            showRadiologyResultModal(requestId);
        });
    });
    
    // Save radiology result button
    const saveRadiologyResultBtn = document.getElementById('saveRadiologyResultBtn');
    if (saveRadiologyResultBtn) {
        saveRadiologyResultBtn.addEventListener('click', function() {
            saveRadiologyResult();
        });
    }
}

/**
 * Show modal for entering radiology result
 * @param {string} requestId - Radiology request ID
 */
function showRadiologyResultModal(requestId) {
    // Get the radiology result modal
    const radiologyResultModal = document.getElementById('radiologyResultModal');
    if (!radiologyResultModal) return;
    
    // Set request ID in the form
    const requestIdInput = radiologyResultModal.querySelector('input[name="request_id"]');
    if (requestIdInput) {
        requestIdInput.value = requestId;
    }
    
    // In a real application, fetch request details from API
    // For now, show the modal with sample data
    
    // Show the modal
    const modal = new bootstrap.Modal(radiologyResultModal);
    modal.show();
}

/**
 * Save radiology result
 */
function saveRadiologyResult() {
    // In a real application, this would submit the form to the API
    // For now, just show an alert and reload
    alert('Hasil radiologi akan disimpan');
    
    // In a real application, update the UI without reloading
    window.location.reload();
}

/**
 * Add a new exam to the radiology request
 */
function addRadiologyExam() {
    const examContainer = document.getElementById('radiologyExamContainer');
    if (!examContainer) return;
    
    const examSelect = document.getElementById('examName');
    const examName = examSelect.options[examSelect.selectedIndex].text;
    const examId = examSelect.value;
    
    if (!examId) {
        alert('Pilih pemeriksaan radiologi terlebih dahulu');
        return;
    }
    
    // Check if exam already exists in the list
    const existingExam = examContainer.querySelector(`[data-exam-id="${examId}"]`);
    if (existingExam) {
        alert('Pemeriksaan ini sudah ditambahkan');
        return;
    }
    
    // Create new exam item
    const examItem = document.createElement('div');
    examItem.className = 'radiology-exam-item d-flex justify-content-between align-items-center p-2 mb-2 bg-light rounded';
    examItem.setAttribute('data-exam-id', examId);
    examItem.innerHTML = `
        <div>
            <i class="fas fa-x-ray me-2"></i> ${examName}
            <input type="hidden" name="exam_ids[]" value="${examId}">
            <input type="hidden" name="exam_names[]" value="${examName}">
        </div>
        <button type="button" class="btn btn-sm btn-outline-danger remove-exam-btn">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add remove functionality
    const removeButton = examItem.querySelector('.remove-exam-btn');
    if (removeButton) {
        removeButton.addEventListener('click', function() {
            examItem.remove();
        });
    }
    
    examContainer.appendChild(examItem);
    
    // Reset exam select
    examSelect.value = '';
}
