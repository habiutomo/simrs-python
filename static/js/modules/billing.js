/**
 * Billing management module for SIMRS
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize billing search
    initBillingSearch();
    
    // Initialize billing items
    initBillingItems();
    
    // Initialize payment processing
    initPaymentProcessing();
    
    // Initialize insurance verification
    initInsuranceVerification();
});

/**
 * Initialize billing search functionality
 */
function initBillingSearch() {
    const searchInput = document.getElementById('searchBilling');
    if (!searchInput) return;
    
    searchInput.addEventListener('keyup', function() {
        const searchText = this.value.toLowerCase();
        const billingTable = document.getElementById('billingTable');
        if (!billingTable) return;
        
        const rows = billingTable.querySelectorAll('tbody tr');
        
        rows.forEach(function(row) {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchText) ? '' : 'none';
        });
    });
}

/**
 * Initialize billing items functionality
 */
function initBillingItems() {
    // Add billing item
    const addItemBtn = document.getElementById('addBillingItemBtn');
    if (addItemBtn) {
        addItemBtn.addEventListener('click', function() {
            addBillingItem();
        });
    }
    
    // Remove billing item
    document.querySelectorAll('.remove-billing-item-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const billingItem = this.closest('.billing-item');
            if (billingItem) {
                billingItem.remove();
                recalculateTotals();
            }
        });
    });
    
    // Quantity and price change events
    document.querySelectorAll('.billing-item input[name="quantity"], .billing-item input[name="unit_price"]').forEach(function(input) {
        input.addEventListener('change', function() {
            updateItemTotal(this.closest('.billing-item'));
            recalculateTotals();
        });
    });
    
    // Insurance covered change
    const insuranceCoveredInput = document.getElementById('insurance_covered');
    if (insuranceCoveredInput) {
        insuranceCoveredInput.addEventListener('change', function() {
            recalculateTotals();
        });
    }
}

/**
 * Add a new billing item to the form
 */
function addBillingItem() {
    const billingContainer = document.getElementById('billingItemsContainer');
    if (!billingContainer) return;
    
    const index = document.querySelectorAll('.billing-item').length;
    
    const newItem = document.createElement('div');
    newItem.className = 'billing-item mb-3 p-3 border rounded';
    newItem.innerHTML = `
        <div class="row">
            <div class="col-md-12 d-flex justify-content-between align-items-center mb-2">
                <h6 class="mb-0">Item #${index + 1}</h6>
                <button type="button" class="btn btn-sm btn-outline-danger remove-billing-item-btn">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
        <div class="row g-2">
            <div class="col-md-6">
                <label class="form-label">Deskripsi</label>
                <input type="text" class="form-control" name="description" required>
            </div>
            <div class="col-md-2">
                <label class="form-label">Jumlah</label>
                <input type="number" class="form-control" name="quantity" value="1" min="1" required>
            </div>
            <div class="col-md-2">
                <label class="form-label">Harga Satuan</label>
                <input type="number" class="form-control" name="unit_price" value="0" min="0" step="1000" required>
            </div>
            <div class="col-md-2">
                <label class="form-label">Total</label>
                <input type="text" class="form-control" name="item_total" value="0" readonly>
            </div>
        </div>
        <div class="row g-2 mt-2">
            <div class="col-md-6">
                <label class="form-label">Tipe Item</label>
                <select class="form-select" name="item_type">
                    <option value="service">Layanan</option>
                    <option value="medication">Obat-obatan</option>
                    <option value="lab">Laboratorium</option>
                    <option value="radiology">Radiologi</option>
                    <option value="room">Kamar/Ruangan</option>
                    <option value="other">Lainnya</option>
                </select>
            </div>
        </div>
    `;
    
    billingContainer.appendChild(newItem);
    
    // Add event listeners to new elements
    const removeButton = newItem.querySelector('.remove-billing-item-btn');
    if (removeButton) {
        removeButton.addEventListener('click', function() {
            newItem.remove();
            recalculateTotals();
        });
    }
    
    const quantityInput = newItem.querySelector('input[name="quantity"]');
    const unitPriceInput = newItem.querySelector('input[name="unit_price"]');
    
    if (quantityInput && unitPriceInput) {
        quantityInput.addEventListener('change', function() {
            updateItemTotal(newItem);
            recalculateTotals();
        });
        
        unitPriceInput.addEventListener('change', function() {
            updateItemTotal(newItem);
            recalculateTotals();
        });
    }
}

/**
 * Update total for a single billing item
 * @param {HTMLElement} itemElement - Billing item element
 */
function updateItemTotal(itemElement) {
    if (!itemElement) return;
    
    const quantityInput = itemElement.querySelector('input[name="quantity"]');
    const unitPriceInput = itemElement.querySelector('input[name="unit_price"]');
    const totalInput = itemElement.querySelector('input[name="item_total"]');
    
    if (!quantityInput || !unitPriceInput || !totalInput) return;
    
    const quantity = parseInt(quantityInput.value) || 0;
    const unitPrice = parseFloat(unitPriceInput.value) || 0;
    const total = quantity * unitPrice;
    
    totalInput.value = total.toFixed(2);
}

/**
 * Recalculate billing totals
 */
function recalculateTotals() {
    // Calculate sum of all items
    let totalAmount = 0;
    
    document.querySelectorAll('.billing-item input[name="item_total"]').forEach(function(input) {
        totalAmount += parseFloat(input.value) || 0;
    });
    
    // Update total amount field
    const totalAmountInput = document.getElementById('total_amount');
    if (totalAmountInput) {
        totalAmountInput.value = totalAmount.toFixed(2);
    }
    
    // Update total amount display
    const totalAmountDisplay = document.getElementById('total_amount_display');
    if (totalAmountDisplay) {
        totalAmountDisplay.textContent = formatCurrency(totalAmount, 'Rp');
    }
    
    // Calculate patient responsibility
    const insuranceCoveredInput = document.getElementById('insurance_covered');
    let insuranceCovered = 0;
    
    if (insuranceCoveredInput) {
        insuranceCovered = parseFloat(insuranceCoveredInput.value) || 0;
    }
    
    const patientResponsibility = Math.max(0, totalAmount - insuranceCovered);
    
    // Update patient responsibility field
    const patientResponsibilityInput = document.getElementById('patient_responsibility');
    if (patientResponsibilityInput) {
        patientResponsibilityInput.value = patientResponsibility.toFixed(2);
    }
    
    // Update patient responsibility display
    const patientResponsibilityDisplay = document.getElementById('patient_responsibility_display');
    if (patientResponsibilityDisplay) {
        patientResponsibilityDisplay.textContent = formatCurrency(patientResponsibility, 'Rp');
    }
}

/**
 * Initialize payment processing functionality
 */
function initPaymentProcessing() {
    // Process payment button
    const processPaymentBtn = document.getElementById('processPaymentBtn');
    if (processPaymentBtn) {
        processPaymentBtn.addEventListener('click', function() {
            const billId = this.getAttribute('data-id');
            showPaymentModal(billId);
        });
    }
    
    // Payment amount input
    const paymentAmountInput = document.getElementById('payment_amount');
    if (paymentAmountInput) {
        paymentAmountInput.addEventListener('change', function() {
            calculateChange();
        });
    }
}

/**
 * Show modal for processing payment
 * @param {string} billId - Billing record ID
 */
function showPaymentModal(billId) {
    // Get the payment modal
    const paymentModal = document.getElementById('paymentModal');
    if (!paymentModal) return;
    
    // Set bill ID in the form
    const billIdInput = paymentModal.querySelector('input[name="bill_id"]');
    if (billIdInput) {
        billIdInput.value = billId;
    }
    
    // In a real application, fetch bill details from API
    // For now, show the modal with sample data
    
    // Show the modal
    const modal = new bootstrap.Modal(paymentModal);
    modal.show();
}

/**
 * Calculate change for payment
 */
function calculateChange() {
    const amountDueInput = document.getElementById('amount_due');
    const paymentAmountInput = document.getElementById('payment_amount');
    const changeDisplay = document.getElementById('change_amount');
    
    if (!amountDueInput || !paymentAmountInput || !changeDisplay) return;
    
    const amountDue = parseFloat(amountDueInput.value) || 0;
    const paymentAmount = parseFloat(paymentAmountInput.value) || 0;
    const change = Math.max(0, paymentAmount - amountDue);
    
    changeDisplay.textContent = formatCurrency(change, 'Rp');
}

/**
 * Initialize insurance verification functionality
 */
function initInsuranceVerification() {
    // Verify insurance button
    const verifyInsuranceBtn = document.getElementById('verifyInsuranceBtn');
    if (verifyInsuranceBtn) {
        verifyInsuranceBtn.addEventListener('click', function() {
            verifyInsurance();
        });
    }
}

/**
 * Verify patient insurance
 */
function verifyInsurance() {
    const patientSelect = document.getElementById('patient_id');
    const insuranceNumberInput = document.getElementById('insurance_number');
    const verificationResult = document.getElementById('insurance_verification_result');
    
    if (!patientSelect || !insuranceNumberInput || !verificationResult) return;
    
    const patientId = patientSelect.value;
    const insuranceNumber = insuranceNumberInput.value;
    
    if (!patientId || !insuranceNumber) {
        verificationResult.innerHTML = '<div class="alert alert-warning">Pilih pasien dan masukkan nomor asuransi</div>';
        return;
    }
    
    // Show loading
    verificationResult.innerHTML = '<div class="d-flex justify-content-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    
    // In a real application, this would be an API call
    // For now, simulate verification
    setTimeout(function() {
        verificationResult.innerHTML = `
            <div class="alert alert-success">
                <strong><i class="fas fa-check-circle"></i> Asuransi terverifikasi</strong><br>
                Nomor: ${insuranceNumber}<br>
                Status: Aktif<br>
                Kelas: 1
            </div>
        `;
        
        // Update insurance covered amount (50% of total for demo)
        const totalAmountInput = document.getElementById('total_amount');
        const insuranceCoveredInput = document.getElementById('insurance_covered');
        
        if (totalAmountInput && insuranceCoveredInput) {
            const totalAmount = parseFloat(totalAmountInput.value) || 0;
            insuranceCoveredInput.value = (totalAmount * 0.5).toFixed(2);
            
            // Recalculate totals
            recalculateTotals();
        }
    }, 1500);
}
