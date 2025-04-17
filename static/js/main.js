/**
 * Main JavaScript file for SIMRS
 */

document.addEventListener('DOMContentLoaded', function() {
    // Toggle sidebar visibility
    const sidebarToggle = document.getElementById('sidebarCollapse');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            const sidebar = document.getElementById('sidebar');
            const content = document.getElementById('content');
            
            sidebar.classList.toggle('active');
            content.classList.toggle('active');
        });
    }
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert.alert-dismissible');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Date field formatting
    document.querySelectorAll('input[type="date"]').forEach(function(dateInput) {
        if (!dateInput.value && !dateInput.getAttribute('data-no-default')) {
            const today = new Date();
            const year = today.getFullYear();
            const month = String(today.getMonth() + 1).padStart(2, '0');
            const day = String(today.getDate()).padStart(2, '0');
            
            dateInput.value = `${year}-${month}-${day}`;
        }
    });
    
    // Time field formatting
    document.querySelectorAll('input[type="time"]').forEach(function(timeInput) {
        if (!timeInput.value && !timeInput.getAttribute('data-no-default')) {
            const today = new Date();
            const hours = String(today.getHours()).padStart(2, '0');
            const minutes = String(Math.ceil(today.getMinutes() / 15) * 15).padStart(2, '0');
            
            timeInput.value = `${hours}:${minutes === '60' ? '00' : minutes}`;
        }
    });
    
    // Search input handling
    document.querySelectorAll('input[type="search"], input[id*="search"]').forEach(function(searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            const tableId = searchInput.getAttribute('data-table') || searchInput.id.replace('search', '') + 'Table';
            const table = document.getElementById(tableId);
            
            if (table) {
                const searchText = searchInput.value.toLowerCase();
                const rows = table.querySelectorAll('tbody tr');
                
                rows.forEach(function(row) {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(searchText) ? '' : 'none';
                });
            }
        });
    });
    
    // Handle dynamic form fields (add/remove)
    const addButtons = document.querySelectorAll('.add-item-btn');
    addButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const templateId = button.getAttribute('data-template');
            const containerId = button.getAttribute('data-container');
            
            if (templateId && containerId) {
                const template = document.getElementById(templateId);
                const container = document.getElementById(containerId);
                
                if (template && container) {
                    const clone = template.content.cloneNode(true);
                    container.appendChild(clone);
                    
                    // Initialize remove buttons for the newly added item
                    initRemoveButtons();
                }
            }
        });
    });
    
    // Initialize remove buttons
    function initRemoveButtons() {
        const removeButtons = document.querySelectorAll('.remove-item-btn');
        removeButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                const item = button.closest('.dynamic-item');
                if (item) {
                    item.remove();
                }
            });
        });
    }
    
    // Initial call to setup remove buttons
    initRemoveButtons();
    
    // Handle confirm dialogs
    document.querySelectorAll('[data-confirm]').forEach(function(element) {
        element.addEventListener('click', function(e) {
            const message = element.getAttribute('data-confirm') || 'Apakah Anda yakin?';
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });
});

/**
 * Format a date string to a more readable format
 * @param {string} dateStr - ISO date string or YYYY-MM-DD
 * @param {string} format - Output format (short, medium, long)
 * @returns {string} Formatted date string
 */
function formatDate(dateStr, format = 'medium') {
    if (!dateStr) return '';
    
    let date;
    if (dateStr.includes('T')) {
        date = new Date(dateStr);
    } else {
        const parts = dateStr.split('-');
        date = new Date(parts[0], parts[1] - 1, parts[2]);
    }
    
    if (isNaN(date.getTime())) return dateStr;
    
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    
    if (format === 'short') {
        options.month = 'numeric';
    } else if (format === 'long') {
        options.weekday = 'long';
    }
    
    return date.toLocaleDateString('id-ID', options);
}

/**
 * Format a datetime string to a more readable format
 * @param {string} datetimeStr - ISO datetime string
 * @param {string} format - Output format (short, medium, long)
 * @returns {string} Formatted datetime string
 */
function formatDateTime(datetimeStr, format = 'medium') {
    if (!datetimeStr) return '';
    
    const date = new Date(datetimeStr);
    if (isNaN(date.getTime())) return datetimeStr;
    
    const dateOptions = { year: 'numeric', month: 'short', day: 'numeric' };
    const timeOptions = { hour: '2-digit', minute: '2-digit' };
    
    if (format === 'short') {
        dateOptions.month = 'numeric';
    } else if (format === 'long') {
        dateOptions.weekday = 'long';
        timeOptions.second = '2-digit';
    }
    
    const dateStr = date.toLocaleDateString('id-ID', dateOptions);
    const timeStr = date.toLocaleTimeString('id-ID', timeOptions);
    
    return `${dateStr} ${timeStr}`;
}

/**
 * Format a currency value
 * @param {number} amount - The amount to format
 * @param {string} currency - The currency symbol
 * @returns {string} Formatted currency string
 */
function formatCurrency(amount, currency = 'Rp') {
    if (amount === null || amount === undefined) return `${currency} 0`;
    
    return `${currency} ${parseFloat(amount).toLocaleString('id-ID', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    })}`;
}

/**
 * Calculate age from birth date
 * @param {string} birthDate - ISO date string or YYYY-MM-DD
 * @returns {number|null} Age in years or null if invalid
 */
function calculateAge(birthDate) {
    if (!birthDate) return null;
    
    let birthDateObj;
    if (birthDate.includes('T')) {
        birthDateObj = new Date(birthDate);
    } else {
        const parts = birthDate.split('-');
        birthDateObj = new Date(parts[0], parts[1] - 1, parts[2]);
    }
    
    if (isNaN(birthDateObj.getTime())) return null;
    
    const today = new Date();
    let age = today.getFullYear() - birthDateObj.getFullYear();
    const monthDiff = today.getMonth() - birthDateObj.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDateObj.getDate())) {
        age--;
    }
    
    return age;
}
