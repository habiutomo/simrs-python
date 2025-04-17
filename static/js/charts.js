/**
 * Chart utility functions for SIMRS
 */

/**
 * Create a bar chart for department visits
 * @param {string} canvasId - Canvas element ID
 * @param {Array} labels - Department names
 * @param {Array} data - Visit counts
 * @param {Object} options - Additional chart options
 */
function createDepartmentVisitsChart(canvasId, labels, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Set default options
    const defaultOptions = {
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return context.parsed.y + ' kunjungan';
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Jumlah Kunjungan'
                },
                ticks: {
                    precision: 0
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Departemen'
                }
            }
        },
        maintainAspectRatio: false,
        responsive: true
    };
    
    // Merge default options with provided options
    const chartOptions = { ...defaultOptions, ...options };
    
    // Create chart
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: chartOptions
    });
}

/**
 * Create a line chart for patient trends
 * @param {string} canvasId - Canvas element ID
 * @param {Array} labels - Date labels
 * @param {Array} data - Patient counts
 * @param {Object} options - Additional chart options
 */
function createPatientTrendChart(canvasId, labels, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Set default options
    const defaultOptions = {
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return context.parsed.y + ' pasien';
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Jumlah Pasien'
                },
                ticks: {
                    precision: 0
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Tanggal'
                }
            }
        },
        maintainAspectRatio: false,
        responsive: true
    };
    
    // Merge default options with provided options
    const chartOptions = { ...defaultOptions, ...options };
    
    // Create chart
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                tension: 0.3,
                fill: true
            }]
        },
        options: chartOptions
    });
}

/**
 * Create a pie chart for data distribution
 * @param {string} canvasId - Canvas element ID
 * @param {Array} labels - Category labels
 * @param {Array} data - Values
 * @param {Array} colors - Background colors
 * @param {Object} options - Additional chart options
 */
function createPieChart(canvasId, labels, data, colors = [], options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Default colors if not provided
    const defaultColors = [
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 99, 132, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 159, 64, 0.7)',
        'rgba(199, 199, 199, 0.7)'
    ];
    
    // Use provided colors or default ones
    const backgroundColor = colors.length > 0 ? colors : defaultColors;
    
    // Set default options
    const defaultOptions = {
        plugins: {
            legend: {
                position: 'right'
            }
        },
        maintainAspectRatio: false,
        responsive: true
    };
    
    // Merge default options with provided options
    const chartOptions = { ...defaultOptions, ...options };
    
    // Create chart
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColor,
                borderWidth: 1
            }]
        },
        options: chartOptions
    });
}

/**
 * Create a doughnut chart for data distribution
 * @param {string} canvasId - Canvas element ID
 * @param {Array} labels - Category labels
 * @param {Array} data - Values
 * @param {Array} colors - Background colors
 * @param {Object} options - Additional chart options
 */
function createDoughnutChart(canvasId, labels, data, colors = [], options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Default colors if not provided
    const defaultColors = [
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 99, 132, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 159, 64, 0.7)',
        'rgba(199, 199, 199, 0.7)'
    ];
    
    // Use provided colors or default ones
    const backgroundColor = colors.length > 0 ? colors : defaultColors;
    
    // Set default options
    const defaultOptions = {
        plugins: {
            legend: {
                position: 'right'
            }
        },
        maintainAspectRatio: false,
        responsive: true,
        cutout: '70%'
    };
    
    // Merge default options with provided options
    const chartOptions = { ...defaultOptions, ...options };
    
    // Create chart
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColor,
                borderWidth: 1
            }]
        },
        options: chartOptions
    });
}
