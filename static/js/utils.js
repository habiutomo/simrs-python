/**
 * Utility functions for SIMRS
 */

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

/**
 * Generate a random ID
 * @param {number} length - Length of the ID
 * @returns {string} Random ID
 */
function generateRandomId(length = 8) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    
    for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    
    return result;
}

/**
 * Validate email address format
 * @param {string} email - Email address to validate
 * @returns {boolean} Whether the email is valid
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Validate phone number format
 * @param {string} phone - Phone number to validate
 * @returns {boolean} Whether the phone number is valid
 */
function validatePhone(phone) {
    // Allow digits, plus, dash, and spaces
    const re = /^[0-9\+\-\s]+$/;
    return re.test(phone) && phone.length >= 8;
}

/**
 * Convert a string to title case
 * @param {string} str - String to convert
 * @returns {string} Title cased string
 */
function toTitleCase(str) {
    if (!str) return '';
    
    return str.replace(
        /\w\S*/g,
        function(txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        }
    );
}

/**
 * Sanitize a string for safe display
 * @param {string} str - String to sanitize
 * @returns {string} Sanitized string
 */
function sanitizeString(str) {
    if (!str) return '';
    
    // Replace potentially dangerous characters
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

/**
 * Get value from URL query parameter
 * @param {string} param - Parameter name
 * @returns {string|null} Parameter value or null if not found
 */
function getUrlParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

/**
 * Set focus to the first invalid field in a form
 * @param {HTMLFormElement} form - Form element
 */
function focusFirstInvalidField(form) {
    if (!form) return;
    
    const invalidField = form.querySelector(':invalid');
    if (invalidField) {
        invalidField.focus();
    }
}
