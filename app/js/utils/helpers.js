
/* ==========================================
   FILE: js/utils/helpers.js
   Utility functions
   ========================================== */

const Helpers = {
    // Show loading indicator
    showLoading() {
        const loading = document.getElementById('loading');
        if (loading) loading.style.display = 'block';
    },

    // Hide loading indicator
    hideLoading() {
        const loading = document.getElementById('loading');
        if (loading) loading.style.display = 'none';
    },

    // Format coordinates
    formatCoordinates(lat, lng) {
        return `${lat.toFixed(4)}°N, ${lng.toFixed(4)}°E`;
    },

    // Get color based on site status
    getStatusColor(status) {
        const colors = window.APP_CONFIG.COLORS;
        return colors[status] || colors.active;
    },

    // Calculate total area from sites
    calculateTotalArea(sites) {
        return sites.reduce((sum, site) => sum + site.area, 0);
    },

    // Count active sites
    countActiveSites(sites) {
        return sites.filter(s => s.status === 'active').length;
    },

    // Count violations
    countViolations(sites) {
        return sites.filter(s => s.illegal).length;
    },

    // Format date and time
    formatDateTime(date = new Date()) {
        return date.toLocaleString('en-IN');
    },

    // Generate unique ID
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    },

    // Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Copy to clipboard
    copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            console.log('Copied to clipboard');
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    },

    // Show notification (simple alert wrapper, can be enhanced)
    notify(message, type = 'info') {
        console.log(`[${type.toUpperCase()}] ${message}`);
        alert(message);
    }
};

// Make helpers globally available
window.Helpers = Helpers;