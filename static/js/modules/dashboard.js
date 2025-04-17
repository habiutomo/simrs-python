/**
 * Dashboard module for SIMRS
 */

document.addEventListener('DOMContentLoaded', function() {
    // Fetch dashboard statistics
    fetchDashboardStatistics();
    
    // Update dashboard data every 5 minutes
    setInterval(fetchDashboardStatistics, 5 * 60 * 1000);
});

/**
 * Fetch dashboard statistics from API
 */
function fetchDashboardStatistics() {
    fetch('/api/dashboard/statistics')
        .then(response => response.json())
        .then(data => {
            updateDashboardStats(data);
            updateDepartmentChart(data.department_visits);
        })
        .catch(error => {
            console.error('Error fetching dashboard statistics:', error);
        });
}

/**
 * Update dashboard statistic cards
 * @param {Object} data - Dashboard statistics data
 */
function updateDashboardStats(data) {
    // Update stat cards if they exist
    const statsToUpdate = [
        { id: 'totalPatients', value: data.total_patients },
        { id: 'appointmentsToday', value: data.appointments_today },
        { id: 'inpatientCount', value: data.inpatient_count },
        { id: 'doctorsOnDuty', value: data.doctors_on_duty }
    ];
    
    statsToUpdate.forEach(stat => {
        const element = document.getElementById(stat.id);
        if (element) {
            element.textContent = stat.value;
        }
    });
}

/**
 * Update department visits chart
 * @param {Array} departmentVisits - Department visit statistics
 */
function updateDepartmentChart(departmentVisits) {
    if (!departmentVisits || !departmentVisits.length) return;
    
    const labels = departmentVisits.map(dept => dept.department);
    const data = departmentVisits.map(dept => dept.visits);
    
    // If chart already exists, destroy it before recreating
    const chartCanvas = document.getElementById('departmentVisitsChart');
    if (chartCanvas && chartCanvas.chart) {
        chartCanvas.chart.destroy();
    }
    
    createDepartmentVisitsChart('departmentVisitsChart', labels, data);
}

/**
 * Create department visits chart
 * @param {string} canvasId - Canvas element ID
 * @param {Array} departments - Department names
 * @param {Array} visitCounts - Visit counts
 */
function createDepartmentVisitsChart(canvasId, departments, visitCounts) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Create chart
    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: departments,
            datasets: [{
                data: visitCounts,
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
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
        }
    });
    
    // Store chart instance on canvas for later reference
    canvas.chart = chart;
}

/**
 * Fetch and display recent activity
 */
function fetchRecentActivities() {
    fetch('/api/activities?limit=5')
        .then(response => response.json())
        .then(activities => {
            updateActivityFeed(activities);
        })
        .catch(error => {
            console.error('Error fetching activities:', error);
        });
}

/**
 * Update activity feed with latest activities
 * @param {Array} activities - Recent activity data
 */
function updateActivityFeed(activities) {
    const activityFeed = document.querySelector('.activity-feed');
    if (!activityFeed) return;
    
    // Clear existing content
    activityFeed.innerHTML = '';
    
    // Add new activities
    activities.forEach(activity => {
        const timestamp = new Date(activity.timestamp);
        const formattedTime = timestamp.toLocaleTimeString('id-ID', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        let iconClass = 'fas fa-cog';
        let bgColor = 'bg-secondary';
        
        // Set icon and color based on action type
        if (activity.action === 'Patient Registration') {
            iconClass = 'fas fa-user-plus';
            bgColor = 'bg-success';
        } else if (activity.action === 'Medical Record Created') {
            iconClass = 'fas fa-file-medical';
            bgColor = 'bg-primary';
        } else if (activity.action === 'Appointment Scheduled') {
            iconClass = 'fas fa-calendar-plus';
            bgColor = 'bg-info';
        } else if (activity.action === 'Payment Recorded') {
            iconClass = 'fas fa-money-bill';
            bgColor = 'bg-warning';
        }
        
        // Create activity item
        const activityItem = document.createElement('div');
        activityItem.className = 'activity-item';
        activityItem.innerHTML = `
            <div class="activity-content">
                <div class="activity-icon ${bgColor}">
                    <i class="${iconClass}"></i>
                </div>
                <div class="activity-text">
                    <p class="mb-0">${activity.details || 'Activity recorded'}</p>
                    <small class="text-muted">${formattedTime}</small>
                </div>
            </div>
        `;
        
        activityFeed.appendChild(activityItem);
    });
}
