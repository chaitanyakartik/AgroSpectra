/* ==========================================
   FILE: js/config.js
   Application configuration and constants
   ========================================== */

const CONFIG = {
    // Map settings
    MAP: {
        DEFAULT_CENTER: [20.5937, 78.9629], // India center
        DEFAULT_ZOOM: 5,
        SITE_ZOOM: 14,
        MIN_ZOOM: 3,
        MAX_ZOOM: 18
    },

    // Tile layer URLs
    TILE_LAYERS: {
        satellite: {
            url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attribution: '© Esri'
        },
        terrain: {
            url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
            attribution: '© OpenTopoMap'
        },
        streets: {
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attribution: '© OpenStreetMap'
        },
        dark: {
            url: 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png',
            attribution: '© Stadia Maps'
        }
    },

    // Status colors
    COLORS: {
        active: {
            border: '#4CAF50',
            fill: '#66BB6A'
        },
        inactive: {
            border: '#9E9E9E',
            fill: '#BDBDBD'
        },
        illegal: {
            border: '#F44336',
            fill: '#EF5350'
        }
    },

    // Layer opacity settings
    OPACITY: {
        DEFAULT: 0.7,
        MIN: 0,
        MAX: 1
    },

    // Update intervals (milliseconds)
    INTERVALS: {
        STATS_UPDATE: 5000,
        AUTO_SAVE: 30000
    },

    // Export formats
    EXPORT_FORMATS: ['GeoJSON', 'KML', 'Shapefile', 'CSV', 'PDF Report'],

    // Detection sensitivity levels
    DETECTION_LEVELS: {
        HIGH: 'high',
        MEDIUM: 'medium',
        LOW: 'low'
    }
};

// Make CONFIG globally available
window.APP_CONFIG = CONFIG;

