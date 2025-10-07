/* ==========================================
   FILE: js/modules/layer-control.js
   Map layers and overlay management
   ========================================== */

const LayerControl = {
    boundaryLayers: [],
    heatmapLayer: null,
    overlayLayers: {},

    // Initialize layer control
    init() {
        console.log('Layer control initialized');
    },

    // Toggle boundary layer
    toggleBoundaryLayer(show) {
        const map = window.MapManager.getMap();
        
        // Remove existing boundaries
        this.boundaryLayers.forEach(layer => map.removeLayer(layer));
        this.boundaryLayers = [];

        if (show) {
            const sites = window.SiteManager.getAllSites();
            
            sites.forEach(site => {
                if (!site.illegal) {
                    // Create slightly larger boundary around legal sites
                    const bounds = L.polygon(site.coordinates).getBounds();
                    const pad = 0.001; // Padding in degrees
                    
                    const boundaryCoords = [
                        [bounds.getSouth() - pad, bounds.getWest() - pad],
                        [bounds.getNorth() + pad, bounds.getWest() - pad],
                        [bounds.getNorth() + pad, bounds.getEast() + pad],
                        [bounds.getSouth() - pad, bounds.getEast() + pad]
                    ];

                    const boundary = L.rectangle(boundaryCoords, {
                        color: '#00FF00',
                        weight: 2,
                        opacity: 0.6,
                        fillOpacity: 0.05,
                        fillColor: '#00FF00',
                        dashArray: '10, 5'
                    }).addTo(map);

                    // Add tooltip
                    boundary.bindTooltip(`Legal Boundary: ${site.name}`, {
                        permanent: false,
                        direction: 'top'
                    });

                    this.boundaryLayers.push(boundary);
                }
            });

            console.log(`Added ${this.boundaryLayers.length} boundary layers`);
        }
    },

    // Toggle heatmap overlay
    toggleHeatmap(show) {
        if (show) {
            this.createHeatmap();
            window.Helpers.notify(
                '🔥 Heatmap Overlay Activated\n\n' +
                'Showing mining activity intensity based on:\n' +
                '• Site area\n' +
                '• Mining volume\n' +
                '• Activity status\n\n' +
                'Red areas indicate highest activity',
                'info'
            );
        } else {
            this.removeHeatmap();
        }
    },

    // Create heatmap visualization
    createHeatmap() {
        const map = window.MapManager.getMap();
        const sites = window.SiteManager.getAllSites();

        // Remove existing heatmap
        this.removeHeatmap();

        // Create circle markers for each site based on activity
        sites.forEach(site => {
            if (site.status === 'active') {
                const intensity = this.calculateIntensity(site);
                const radius = Math.sqrt(site.area) * 1000; // Radius based on area

                const heatCircle = L.circle(site.location, {
                    radius: radius,
                    color: this.getHeatColor(intensity),
                    fillColor: this.getHeatColor(intensity),
                    fillOpacity: 0.4,
                    weight: 1,
                    opacity: 0.6
                }).addTo(map);

                if (!this.overlayLayers.heatmap) {
                    this.overlayLayers.heatmap = [];
                }
                this.overlayLayers.heatmap.push(heatCircle);
            }
        });
    },

    // Calculate activity intensity (0-1)
    calculateIntensity(site) {
        // Intensity based on area and volume
        const maxArea = 20; // hectares
        const maxVolume = 6; // M m³
        
        const areaScore = Math.min(site.area / maxArea, 1);
        const volumeScore = Math.min(site.volume / maxVolume, 1);
        const statusScore = site.status === 'active' ? 1 : 0.5;
        
        return (areaScore * 0.4 + volumeScore * 0.4 + statusScore * 0.2);
    },

    // Get color based on intensity
    getHeatColor(intensity) {
        // Color gradient from yellow to red
        if (intensity > 0.8) return '#FF0000'; // Red - Very high
        if (intensity > 0.6) return '#FF4500'; // Orange-red - High
        if (intensity > 0.4) return '#FF8C00'; // Dark orange - Medium-high
        if (intensity > 0.2) return '#FFA500'; // Orange - Medium
        return '#FFD700'; // Gold - Low
    },

    // Remove heatmap
    removeHeatmap() {
        const map = window.MapManager.getMap();
        
        if (this.overlayLayers.heatmap) {
            this.overlayLayers.heatmap.forEach(layer => {
                map.removeLayer(layer);
            });
            this.overlayLayers.heatmap = [];
        }
    },

    // Change base layer
    changeBaseLayer(layerType) {
        window.MapManager.changeBaseLayer(layerType);
        console.log(`Base layer changed to: ${layerType}`);
    },

    // Add custom overlay
    addOverlay(name, layer) {
        const map = window.MapManager.getMap();
        
        if (!this.overlayLayers[name]) {
            this.overlayLayers[name] = [];
        }
        
        this.overlayLayers[name].push(layer);
        layer.addTo(map);
    },

    // Remove custom overlay
    removeOverlay(name) {
        const map = window.MapManager.getMap();
        
        if (this.overlayLayers[name]) {
            this.overlayLayers[name].forEach(layer => {
                map.removeLayer(layer);
            });
            delete this.overlayLayers[name];
        }
    },

    // Toggle overlay visibility
    toggleOverlay(name, show) {
        const map = window.MapManager.getMap();
        
        if (this.overlayLayers[name]) {
            this.overlayLayers[name].forEach(layer => {
                if (show) {
                    layer.addTo(map);
                } else {
                    map.removeLayer(layer);
                }
            });
        }
    },

    // Clear all overlays
    clearAllOverlays() {
        const map = window.MapManager.getMap();
        
        // Clear boundaries
        this.boundaryLayers.forEach(layer => map.removeLayer(layer));
        this.boundaryLayers = [];
        
        // Clear heatmap
        this.removeHeatmap();
        
        // Clear custom overlays
        Object.keys(this.overlayLayers).forEach(name => {
            this.removeOverlay(name);
        });
        
        console.log('All overlays cleared');
    },

    // Get all active overlays
    getActiveOverlays() {
        return Object.keys(this.overlayLayers).filter(name => {
            return this.overlayLayers[name] && this.overlayLayers[name].length > 0;
        });
    }
};

// Make LayerControl globally available
window.LayerControl = LayerControl;