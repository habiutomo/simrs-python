/**
 * Patient management module for SIMRS
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize patient search
    initPatientSearch();
    
    // Initialize BPJS verification
    initBPJSVerification();
    
    // Initialize age calculation
    initAgeCalculation();
});

/**
 * Initialize patient search functionality
 */
function initPatientSearch() {
    const searchInput = document.getElementById('searchPatient');
    if (!searchInput) return;
    
    searchInput.addEventListener('keyup', function() {
        const searchText = this.value.toLowerCase();
        const patientTable = document.getElementById('patientTable');
        if (!patientTable) return;
        
        const rows = patientTable.querySelectorAll('tbody tr');
        
        rows.forEach(function(row) {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchText) ? '' : 'none';
        });
    });
}

/**
 * Initialize BPJS insurance verification
 */
function initBPJSVerification() {
    const verifyButton = document.getElementById('verifyBPJS');
    if (!verifyButton) return;
    
    verifyButton.addEventListener('click', function() {
        const insuranceNumber = document.getElementById('insurance_number').value;
        const insuranceProvider = document.getElementById('insurance_provider').value;
        const statusElement = document.getElementById('bpjsStatus');
        
        if (!insuranceNumber || insuranceProvider !== 'BPJS') {
            if (statusElement) {
                statusElement.innerHTML = '<span class="text-danger">Masukkan nomor BPJS dan pilih BPJS sebagai penyedia asuransi</span>';
            }
            return;
        }
        
        // Show loading status
        if (statusElement) {
            statusElement.innerHTML = '<span class="text-info">Memverifikasi nomor BPJS...</span>';
        }
        
        // Call BPJS verification API
        fetch(`/api/bpjs/verify?insurance_number=${insuranceNumber}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'active') {
                    if (statusElement) {
                        statusElement.innerHTML = `
                            <span class="text-success">
                                <i class="fas fa-check-circle"></i> Nomor BPJS terverifikasi: ${data.member_name} (Kelas ${data.class})
                            </span>
                        `;
                    }
                } else {
                    if (statusElement) {
                        statusElement.innerHTML = `
                            <span class="text-danger">
                                <i class="fas fa-times-circle"></i> Nomor BPJS tidak valid: ${data.error || 'Nomor tidak ditemukan'}
                            </span>
                        `;
                    }
                }
            })
            .catch(error => {
                console.error('Error verifying BPJS:', error);
                if (statusElement) {
                    statusElement.innerHTML = '<span class="text-danger">Gagal memverifikasi: Terjadi kesalahan sistem</span>';
                }
            });
    });
    
    // Auto-verify when changing insurance provider to BPJS
    const insuranceProviderSelect = document.getElementById('insurance_provider');
    if (insuranceProviderSelect) {
        insuranceProviderSelect.addEventListener('change', function() {
            const insuranceNumber = document.getElementById('insurance_number').value;
            if (this.value === 'BPJS' && insuranceNumber) {
                verifyButton.click();
            }
        });
    }
}

/**
 * Initialize automatic age calculation from birth date
 */
function initAgeCalculation() {
    const birthDateInput = document.getElementById('birth_date');
    const ageDisplay = document.getElementById('age_display');
    
    if (birthDateInput && ageDisplay) {
        // Calculate age on page load
        if (birthDateInput.value) {
            updateAgeDisplay(birthDateInput.value, ageDisplay);
        }
        
        // Update age when birth date changes
        birthDateInput.addEventListener('change', function() {
            updateAgeDisplay(this.value, ageDisplay);
        });
    }
}

/**
 * Update age display based on birth date
 * @param {string} birthDate - Birth date string (YYYY-MM-DD)
 * @param {HTMLElement} displayElement - Element to display age
 */
function updateAgeDisplay(birthDate, displayElement) {
    if (!birthDate) {
        displayElement.textContent = '';
        return;
    }
    
    const age = calculateAge(birthDate);
    if (age !== null) {
        displayElement.textContent = `${age} tahun`;
    } else {
        displayElement.textContent = '';
    }
}

/**
 * Add allergy to patient form
 */
function addAllergy() {
    const allergyInput = document.getElementById('allergy_input');
    const allergiesList = document.getElementById('allergies_list');
    const allergiesHidden = document.getElementById('allergies');
    
    if (!allergyInput || !allergiesList || !allergiesHidden) return;
    
    const allergy = allergyInput.value.trim();
    if (!allergy) return;
    
    // Create new allergy badge
    const allergyItem = document.createElement('span');
    allergyItem.className = 'badge bg-danger me-1 mb-1';
    allergyItem.textContent = allergy;
    
    // Add remove button
    const removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.className = 'btn-close btn-close-white ms-1';
    removeButton.style.fontSize = '0.5rem';
    removeButton.setAttribute('aria-label', 'Remove');
    removeButton.addEventListener('click', function() {
        allergyItem.remove();
        updateAllergiesHidden();
    });
    
    allergyItem.appendChild(removeButton);
    allergiesList.appendChild(allergyItem);
    
    // Clear input
    allergyInput.value = '';
    
    // Update hidden field
    updateAllergiesHidden();
}

/**
 * Update hidden allergies field with current values
 */
function updateAllergiesHidden() {
    const allergiesList = document.getElementById('allergies_list');
    const allergiesHidden = document.getElementById('allergies');
    
    if (!allergiesList || !allergiesHidden) return;
    
    const allergies = [];
    allergiesList.querySelectorAll('.badge').forEach(function(badge) {
        // Get text content excluding the close button text
        const allergyText = badge.childNodes[0].nodeValue;
        allergies.push(allergyText.trim());
    });
    
    allergiesHidden.value = allergies.join(',');
}
