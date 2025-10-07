/* ==========================================
   FILE: js/modules/site-manager.js
   Mining site operations and management
   ========================================== */

const SiteManager = {
    sites: [],
    miningLayers: [],
    selectedSite: null,

    // Initialize with sites data
    init(sitesData) {
        this.sites = sitesData || window.MINING_SITES_DATA || [];
        this.loadSitesOnMap();
        this.populateSitesList();
        console.log(`Loaded ${this.sites.length} mining sites`);
    },

    // Load all sites on the map
    loadSitesOnMap() {
        const map = window.MapManager.getMap();
        
        this.sites.forEach(site => {
            const colors = window.Helpers.getStatusColor(site.status);

            // Create polygon for mining area
            const polygon = L.polygon(site.coordinates, {
                color: colors.border,
                weight: 3,
                opacity: 0.8,
                fillOpacity: 0.3,
                fillColor: colors.fill
            }).addTo(map);

            // Create popup content
            const popupContent = this.createPopupContent(site);
            polygon.bindPopup(popupContent);

            // Add click event
            polygon.on('click', () => this.selectSite(site));

            // Store reference
            site.polygon = polygon;
            this.miningLayers.push(polygon);

            // Add marker for better visibility
            const marker = L.circleMarker(site.location, {
                radius: 6,
                fillColor: colors.border,
                color: "#fff",
                weight: 2,
                opacity: 1,
                fillOpacity: 0.8
            }).addTo(map);

            marker.on('click', () => {
                window.MapManager.panTo(site.location, window.APP_CONFIG.MAP.SITE_ZOOM);
                this.selectSite(site);
            });

            // Store marker reference
            site.marker = marker;
        });
    },

    // Create popup content HTML
    createPopupContent(site) {
        const colors = window.Helpers.getStatusColor(site.status);
        return `
            <div style="min-width: 200px;">
                <h4 style="margin: 0 0 10px 0; color: ${colors.border};">${site.name}</h4>
                <table style="width: 100%; font-size: 12px;">
                    <tr><td><b>Type:</b></td><td>${site.type}</td></tr>
                    <tr><td><b>Status:</b></td><td>${site.status.toUpperCase()}</td></tr>
                    <tr><td><b>Operator:</b></td><td>${site.operator}</td></tr>
                    <tr><td><b>Area:</b></td><td>${site.area} ha</td></tr>
                    <tr><td><b>Depth:</b></td><td>${site.depth} m</td></tr>
                    <tr><td><b>Volume:</b></td><td>${site.volume} M m³</td></tr>
                </table>
            </div>
        `;
    },

    // Populate sites list in sidebar
    populateSitesList() {
        const sitesList = document.getElementById('sitesList');
        if (!sitesList) return;

        sitesList.innerHTML = '';

        this.sites.forEach(site => {
            const siteItem = document.createElement('div');
            siteItem.className = 'site-item';
            siteItem.setAttribute('data-site-id', site.id);
            
            siteItem.onclick = () => {
                window.MapManager.panTo(site.location, window.APP_CONFIG.MAP.SITE_ZOOM);
                this.selectSite(site);
            };

            let statusClass = 'status-active';
            if (site.status === 'inactive') statusClass = 'status-inactive';
            if (site.status === 'illegal') statusClass = 'status-illegal';

            siteItem.innerHTML = `
                <div class="site-name">${site.name}</div>
                <div class="site-details">
                    <span>${site.type} • ${site.area} ha</span>
                    <span class="status-badge ${statusClass}">${site.status}</span>
                </div>
            `;

            sitesList.appendChild(siteItem);
        });
    },

    // Select a mining site
    selectSite(site) {
        this.selectedSite = site;
        
        // Update visual state of site items
        document.querySelectorAll('.site-item').forEach(item => {
            const itemId = parseInt(item.getAttribute('data-site-id'));
            if (itemId === site.id) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });

        // Update info panel
        this.updateInfoPanel(site);
        
        // Highlight selected polygon
        this.highlightSite(site);

        // Open popup
        if (site.polygon) {
            site.polygon.openPopup();
        }
    },

    // Highlight selected site on map
    highlightSite(site) {
        this.miningLayers.forEach(layer => {
            layer.setStyle({ weight: 3 });
        });
        if (site.polygon) {
            site.polygon.setStyle({ weight: 5 });
            site.polygon.bringToFront();
        }
    },

    // Update info panel with site details
    updateInfoPanel(site) {
        const siteInfo = document.getElementById('siteInfo');
        if (!siteInfo) return;

        const colors = window.Helpers.getStatusColor(site.status);

        siteInfo.innerHTML = `
            <div class="info-row">
                <span class="info-label">Name:</span>
                <span class="info-value">${site.name}</span>
            </div>
            <div class="info-row">
                <span class="info-label">ID:</span>
                <span class="info-value">#${site.id.toString().padStart(5, '0')}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Type:</span>
                <span class="info-value">${site.type}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Location:</span>
                <span class="info-value">${window.Helpers.formatCoordinates(site.location[0], site.location[1])}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Status:</span>
                <span class="info-value" style="color: ${colors.border}; font-weight: bold;">${site.status.toUpperCase()}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Operator:</span>
                <span class="info-value">${site.operator}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Mining Area:</span>
                <span class="info-value">${site.area} hectares</span>
            </div>
            <div class="info-row">
                <span class="info-label">Average Depth:</span>
                <span class="info-value">${site.depth} meters</span>
            </div>
            <div class="info-row">
                <span class="info-label">Estimated Volume:</span>
                <span class="info-value">${site.volume} M m³</span>
            </div>
            ${site.illegal ? `
            <div class="info-row">
                <span class="info-label">Violation:</span>
                <span class="info-value" style="color: #F44336;">⚠️ Illegal Mining Detected</span>
            </div>
            ` : ''}
        `;
    },

    // Get selected site
    getSelectedSite() {
        return this.selectedSite;
    },

    // Get all sites
    getAllSites() {
        return this.sites;
    },

    // Get sites by status
    getSitesByStatus(status) {
        return this.sites.filter(site => site.status === status);
    },

    // Get illegal sites
    getIllegalSites() {
        return this.sites.filter(site => site.illegal);
    },

    // Get mining layers
    getMiningLayers() {
        return this.miningLayers;
    },

    // Toggle mining overlay visibility
    toggleOverlay(show) {
        this.miningLayers.forEach(layer => {
            layer.setStyle({ opacity: show ? 0.8 : 0, fillOpacity: show ? 0.3 : 0 });
        });
    },

    // Update layer opacity
    updateOpacity(value) {
        const opacity = value / 100;
        this.miningLayers.forEach(layer => {
            layer.setStyle({ 
                fillOpacity: opacity * 0.5,
                opacity: opacity * 0.8 
            });
        });
    },

    // Add new site
    addSite(siteData) {
        this.sites.push(siteData);
        // Reload map and list
        this.loadSitesOnMap();
        this.populateSitesList();
    },

    // Remove site by ID
    removeSite(siteId) {
        const siteIndex = this.sites.findIndex(s => s.id === siteId);
        if (siteIndex !== -1) {
            const site = this.sites[siteIndex];
            
            // Remove from map
            if (site.polygon) {
                window.MapManager.removeLayer(site.polygon);
            }
            if (site.marker) {
                window.MapManager.removeLayer(site.marker);
            }
            
            // Remove from array
            this.sites.splice(siteIndex, 1);
            
            // Update list
            this.populateSitesList();
        }
    },

    // Clear selection
    clearSelection() {
        this.selectedSite = null;
        document.querySelectorAll('.site-item').forEach(item => {
            item.classList.remove('active');
        });
        this.miningLayers.forEach(layer => {
            layer.setStyle({ weight: 3 });
        });
    }
};

// Make SiteManager globally available
window.SiteManager = SiteManager;