/* ==========================================
   FILE: js/core/map-manager.js
   Map initialization and core functionality
   ========================================== */

const MapManager = {
    map: null,
    currentBaseLayer: null,
    drawnItems: null,

    // Initialize the map
    init() {
        const config = window.APP_CONFIG.MAP;
        
        this.map = L.map('map', {
            center: config.DEFAULT_CENTER,
            zoom: config.DEFAULT_ZOOM,
            zoomControl: false
        });

        // Add zoom control to bottom right
        L.control.zoom({
            position: 'bottomright'
        }).addTo(this.map);

        // Add scale control
        L.control.scale({
            position: 'bottomleft'
        }).addTo(this.map);

        // Initialize drawing controls
        this.drawnItems = new L.FeatureGroup();
        this.map.addLayer(this.drawnItems);

        // Set default base layer
        this.changeBaseLayer('satellite');

        // Handle resize
        window.addEventListener('resize', () => {
            if (this.map) {
                this.map.invalidateSize();
            }
        });

        console.log('Map initialized successfully');
        return this.map;
    },

    // Change base map layer
    changeBaseLayer(layerType) {
        if (this.currentBaseLayer) {
            this.map.removeLayer(this.currentBaseLayer);
        }

        const layerConfig = window.APP_CONFIG.TILE_LAYERS[layerType];
        if (layerConfig) {
            this.currentBaseLayer = L.tileLayer(layerConfig.url, {
                attribution: layerConfig.attribution
            });
            this.currentBaseLayer.addTo(this.map);
        }
    },

    // Get map instance
    getMap() {
        return this.map;
    },

    // Pan to location with optional zoom
    panTo(location, zoom = null) {
        if (zoom) {
            this.map.setView(location, zoom);
        } else {
            this.map.panTo(location);
        }
    },

    // Fit bounds to show all features
    fitBounds(bounds, options = {}) {
        this.map.fitBounds(bounds, options);
    },

    // Get current map center
    getCenter() {
        return this.map.getCenter();
    },

    // Get current zoom level
    getZoom() {
        return this.map.getZoom();
    },

    // Get drawn items layer
    getDrawnItems() {
        return this.drawnItems;
    },

    // Add layer to map
    addLayer(layer) {
        layer.addTo(this.map);
    },

    // Remove layer from map
    removeLayer(layer) {
        this.map.removeLayer(layer);
    },

    // Clear all drawn items
    clearDrawnItems() {
        this.drawnItems.clearLayers();
    }
};

// Make MapManager globally available
window.MapManager = MapManager;