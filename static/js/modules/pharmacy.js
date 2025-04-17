/**
 * Pharmacy management module for SIMRS
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize prescription search
    initPrescriptionSearch();
    
    // Initialize inventory management
    initInventoryManagement();
    
    // Initialize prescription dispensing
    initPrescriptionDispensing();
});

/**
 * Initialize prescription search functionality
 */
function initPrescriptionSearch() {
    const searchInput = document.getElementById('searchPrescription');
    if (!searchInput) return;
    
    searchInput.addEventListener('keyup', function() {
        const searchText = this.value.toLowerCase();
        const prescriptionTable = document.getElementById('prescriptionTable');
        if (!prescriptionTable) return;
        
        const rows = prescriptionTable.querySelectorAll('tbody tr');
        
        rows.forEach(function(row) {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchText) ? '' : 'none';
        });
    });
}

/**
 * Initialize inventory management functionality
 */
function initInventoryManagement() {
    // Add inventory item
    const addInventoryBtn = document.getElementById('addInventoryBtn');
    if (addInventoryBtn) {
        addInventoryBtn.addEventListener('click', function() {
            showAddInventoryModal();
        });
    }
    
    // Update inventory item
    document.querySelectorAll('.update-inventory-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const itemId = this.getAttribute('data-id');
            showUpdateInventoryModal(itemId);
        });
    });
    
    // Inventory alert notification
    checkLowInventory();
}

/**
 * Initialize prescription dispensing functionality
 */
function initPrescriptionDispensing() {
    // Mark prescription as dispensed
    document.querySelectorAll('.dispense-prescription-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const prescriptionId = this.getAttribute('data-id');
            dispensePrescription(prescriptionId);
        });
    });
}

/**
 * Show modal for adding new inventory item
 */
function showAddInventoryModal() {
    // Get the inventory modal
    const inventoryModal = document.getElementById('inventoryModal');
    if (!inventoryModal) return;
    
    // Reset form
    const inventoryForm = inventoryModal.querySelector('form');
    if (inventoryForm) {
        inventoryForm.reset();
    }
    
    // Set title
    const modalTitle = inventoryModal.querySelector('.modal-title');
    if (modalTitle) {
        modalTitle.textContent = 'Tambah Item Inventaris';
    }
    
    // Show the modal
    const modal = new bootstrap.Modal(inventoryModal);
    modal.show();
}

/**
 * Show modal for updating inventory item
 * @param {string} itemId - Inventory item ID
 */
function showUpdateInventoryModal(itemId) {
    // Get the inventory modal
    const inventoryModal = document.getElementById('inventoryModal');
    if (!inventoryModal) return;
    
    // Set title
    const modalTitle = inventoryModal.querySelector('.modal-title');
    if (modalTitle) {
        modalTitle.textContent = 'Update Item Inventaris';
    }
    
    // In a real application, fetch item details from API
    // For now, just show the modal with empty form
    const modal = new bootstrap.Modal(inventoryModal);
    modal.show();
}

/**
 * Mark prescription as dispensed
 * @param {string} prescriptionId - Prescription ID
 */
function dispensePrescription(prescriptionId) {
    // In a real application, this would be an API call
    // For now, just show an alert and reload
    alert('Resep akan ditandai sebagai telah dikeluarkan');
    
    // In a real application, update the UI without reloading
    window.location.reload();
}

/**
 * Check for low inventory items and show notification
 */
function checkLowInventory() {
    // In a real application, this would check inventory levels from the API
    // For now, just simulate a notification
    
    // Get notification area
    const notificationArea = document.getElementById('inventoryAlerts');
    if (!notificationArea) return;
    
    // Add a sample notification
    notificationArea.innerHTML = `
        <div class="alert alert-warning alert-dismissible fade show" role="alert">
            <strong><i class="fas fa-exclamation-triangle"></i> Peringatan Inventaris Rendah:</strong> 
            Beberapa item inventaris sudah mencapai batas minimum.
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}
