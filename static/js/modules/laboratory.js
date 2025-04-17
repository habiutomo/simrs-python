/**
 * Laboratory management module for SIMRS
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize lab request search
    initLabRequestSearch();
    
    // Initialize lab test categories
    initLabTestCategories();
    
    // Initialize lab result entry
    initLabResultEntry();
});

/**
 * Initialize lab request search functionality
 */
function initLabRequestSearch() {
    const searchInput = document.getElementById('searchLabRequest');
    if (!searchInput) return;
    
    searchInput.addEventListener('keyup', function() {
        const searchText = this.value.toLowerCase();
        const labRequestTable = document.getElementById('labRequestTable');
        if (!labRequestTable) return;
        
        const rows = labRequestTable.querySelectorAll('tbody tr');
        
        rows.forEach(function(row) {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchText) ? '' : 'none';
        });
    });
}

/**
 * Initialize lab test categories functionality
 */
function initLabTestCategories() {
    const categorySelect = document.getElementById('testCategory');
    const testSelect = document.getElementById('testName');
    
    if (!categorySelect || !testSelect) return;
    
    categorySelect.addEventListener('change', function() {
        const category = this.value;
        
        // Reset test select
        testSelect.innerHTML = '<option value="">Pilih tes lab...</option>';
        
        if (!category) return;
        
        // In a real application, this would fetch tests for the selected category
        // For now, simulate loading
        testSelect.disabled = true;
        
        setTimeout(function() {
            // Re-enable the select
            testSelect.disabled = false;
            
            // Add sample tests based on category (would come from API in real app)
            let tests = [];
            
            if (category === 'hematology') {
                tests = [
                    { id: 'h1', name: 'Hemoglobin' },
                    { id: 'h2', name: 'Hematokrit' },
                    { id: 'h3', name: 'Trombosit' },
                    { id: 'h4', name: 'Leukosit' }
                ];
            } else if (category === 'biochemistry') {
                tests = [
                    { id: 'b1', name: 'Gula Darah Puasa' },
                    { id: 'b2', name: 'Kolesterol Total' },
                    { id: 'b3', name: 'HDL' },
                    { id: 'b4', name: 'LDL' }
                ];
            } else if (category === 'urine') {
                tests = [
                    { id: 'u1', name: 'Urinalisis Lengkap' },
                    { id: 'u2', name: 'Protein Urin' },
                    { id: 'u3', name: 'Glukosa Urin' }
                ];
            }
            
            tests.forEach(function(test) {
                const option = document.createElement('option');
                option.value = test.id;
                option.textContent = test.name;
                testSelect.appendChild(option);
            });
        }, 500);
    });
}

/**
 * Initialize lab result entry functionality
 */
function initLabResultEntry() {
    // Process lab request button
    document.querySelectorAll('.process-lab-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const requestId = this.getAttribute('data-id');
            showLabResultModal(requestId);
        });
    });
    
    // Save lab result button
    const saveLabResultBtn = document.getElementById('saveLabResultBtn');
    if (saveLabResultBtn) {
        saveLabResultBtn.addEventListener('click', function() {
            saveLabResult();
        });
    }
}

/**
 * Show modal for entering lab result
 * @param {string} requestId - Lab request ID
 */
function showLabResultModal(requestId) {
    // Get the lab result modal
    const labResultModal = document.getElementById('labResultModal');
    if (!labResultModal) return;
    
    // Set request ID in the form
    const requestIdInput = labResultModal.querySelector('input[name="request_id"]');
    if (requestIdInput) {
        requestIdInput.value = requestId;
    }
    
    // In a real application, fetch request details from API
    // For now, show the modal with sample data
    
    // Show the modal
    const modal = new bootstrap.Modal(labResultModal);
    modal.show();
}

/**
 * Save lab result
 */
function saveLabResult() {
    // In a real application, this would submit the form to the API
    // For now, just show an alert and reload
    alert('Hasil laboratorium akan disimpan');
    
    // In a real application, update the UI without reloading
    window.location.reload();
}

/**
 * Add a new test to the lab request
 */
function addLabTest() {
    const testContainer = document.getElementById('labTestContainer');
    if (!testContainer) return;
    
    const testSelect = document.getElementById('testName');
    const testName = testSelect.options[testSelect.selectedIndex].text;
    const testId = testSelect.value;
    
    if (!testId) {
        alert('Pilih tes lab terlebih dahulu');
        return;
    }
    
    // Check if test already exists in the list
    const existingTest = testContainer.querySelector(`[data-test-id="${testId}"]`);
    if (existingTest) {
        alert('Tes ini sudah ditambahkan');
        return;
    }
    
    // Create new test item
    const testItem = document.createElement('div');
    testItem.className = 'lab-test-item d-flex justify-content-between align-items-center p-2 mb-2 bg-light rounded';
    testItem.setAttribute('data-test-id', testId);
    testItem.innerHTML = `
        <div>
            <i class="fas fa-flask me-2"></i> ${testName}
            <input type="hidden" name="test_ids[]" value="${testId}">
            <input type="hidden" name="test_names[]" value="${testName}">
        </div>
        <button type="button" class="btn btn-sm btn-outline-danger remove-test-btn">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add remove functionality
    const removeButton = testItem.querySelector('.remove-test-btn');
    if (removeButton) {
        removeButton.addEventListener('click', function() {
            testItem.remove();
        });
    }
    
    testContainer.appendChild(testItem);
    
    // Reset test select
    testSelect.value = '';
}
