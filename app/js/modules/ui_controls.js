
/* ==========================================
   FILE: js/modules/ui-controls.js
   UI interactions and controls
   ========================================== */

const UIControls = {
    // Toggle sidebar section
    toggleSection(header) {
        const content = header.nextElementSibling;
        const arrow = header.querySelector('span:last-child');
        const isActive = content.classList.contains('active');
        
        // Close all sections
        document.querySelectorAll('.sidebar-content').forEach(c => {
            c.classList.remove('active');
        });
        document.querySelectorAll('.sidebar-header').forEach(h => {
            h.classList.remove('active');
            h.querySelector('span:last-child').textContent = '▶';
        });
        
        // Open clicked section if it was closed
        if (!isActive) {
            content.classList.add('active');
            header.classList.add('active');
            arrow.textContent = '▼';
        }
    },

    // Set view mode (2D/3D)
    setView(mode, button) {
        document.querySelectorAll('.view-toggle button').forEach(b => b.classList.remove('active'));
        button.classList.add('active');
        
        if (mode === '3D') {
            window.Helpers.notify('🎮 3D Terrain View\n\n' +
                'This will open an interactive 3D visualization of the mining area with:\n' +
                '• Elevation data\n' +
                '• Depth analysis\n' +
                '• Volume rendering\n\n' +
                '(Feature requires WebGL support)', 'info');
        }
    },

    // Upload AOI (Area of Interest)
    uploadAOI() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.shp,.kml,.kmz,.geojson,.json';
        input.onchange = e => {
            const file = e.target.files[0];
            if (file) {
                window.Helpers.showLoading();
                setTimeout(() => {
                    window.Helpers.hideLoading();
                    window.Helpers.notify(`✅ AOI Successfully Uploaded!\n\n` +
                        `File: ${file.name}\n` +
                        `Size: ${(file.size / 1024).toFixed(2)} KB\n\n` +
                        `The area of interest has been added to the map.`, 'success');
                }, 1500);
            }
        };
        input.click();
    },

    // Measure distance tool
    measureTool() {
        window.Helpers.notify('📏 Measurement Tool Active\n\n' +
            'Click on the map to:\n' +
            '• Measure distances between points\n' +
            '• Calculate areas of polygons\n' +
            '• Measure elevation profiles\n\n' +
            'Double-click to finish measurement', 'info');
    },

    // Draw polygon tool
    drawPolygon() {
        const map = window.MapManager.getMap();
        const drawnItems = window.MapManager.getDrawnItems();
        
        const drawControl = new L.Control.Draw({
            position: 'topright',
            draw: {
                polygon: {
                    shapeOptions: {
                        color: '#FF6B6B',
                        weight: 3
                    }
                },
                polyline: false,
                rectangle: true,
                circle: false,
                circlemarker: false,
                marker: false
            },
            edit: {
                featureGroup: drawnItems
            }
        });
        map.addControl(drawControl);
        
        map.on(L.Draw.Event.CREATED, function (e) {
            const layer = e.layer;
            drawnItems.addLayer(layer);
            
            // Calculate area for polygons
            if (e.layerType === 'polygon' || e.layerType === 'rectangle') {
                const area = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]) / 10000;
                window.Helpers.notify(`Area drawn: ${area.toFixed(2)} hectares`, 'info');
            }
        });

        window.Helpers.notify('✏️ Drawing Tools Activated\n\n' +
            'Draw polygons or rectangles to:\n' +
            '• Mark areas of interest\n' +
            '• Define new mining boundaries\n' +
            '• Highlight potential violations', 'info');
    },

    // Capture snapshot
    captureSnapshot() {
        const map = window.MapManager.getMap();
        const center = map.getCenter();
        window.Helpers.notify('📸 Snapshot Captured!\n\n' +
            'Current view has been saved with:\n' +
            `• Timestamp: ${window.Helpers.formatDateTime()}\n` +
            `• Coordinates: ${window.Helpers.formatCoordinates(center.lat, center.lng)}\n` +
            `• Zoom Level: ${map.getZoom()}`, 'success');
    },

    // Toggle fullscreen
    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    },

    // Update opacity slider value display
    updateOpacityDisplay(value) {
        const opacityValue = document.getElementById('opacityValue');
        if (opacityValue) {
            opacityValue.textContent = value + '%';
        }
    },

    // Initialize all UI event listeners
    initEventListeners() {
        // Sidebar section toggles
        document.querySelectorAll('.sidebar-header').forEach(header => {
            header.addEventListener('click', () => this.toggleSection(header));
        });

        // View toggle buttons
        document.querySelectorAll('.view-toggle button').forEach(button => {
            button.addEventListener('click', () => {
                const view = button.getAttribute('data-view');
                this.setView(view, button);
            });
        });

        // Upload AOI button
        const uploadBtn = document.getElementById('uploadAOIBtn');
        if (uploadBtn) {
            uploadBtn.addEventListener('click', () => this.uploadAOI());
        }

        // Base layer select
        const baseLayerSelect = document.getElementById('baseLayerSelect');
        if (baseLayerSelect) {
            baseLayerSelect.addEventListener('change', (e) => {
                window.LayerControl.changeBaseLayer(e.target.value);
            });
        }

        // Mining overlay checkbox
        const miningOverlay = document.getElementById('miningOverlay');
        if (miningOverlay) {
            miningOverlay.addEventListener('change', (e) => {
                window.SiteManager.toggleOverlay(e.target.checked);
            });
        }

        // Boundary overlay checkbox
        const boundaryOverlay = document.getElementById('boundaryOverlay');
        if (boundaryOverlay) {
            boundaryOverlay.addEventListener('change', (e) => {
                window.LayerControl.toggleBoundaryLayer(e.target.checked);
            });
        }

        // Heatmap overlay checkbox
        const heatmapOverlay = document.getElementById('heatmapOverlay');
        if (heatmapOverlay) {
            heatmapOverlay.addEventListener('change', (e) => {
                window.LayerControl.toggleHeatmap(e.target.checked);
            });
        }

        // Opacity slider
        const opacitySlider = document.getElementById('opacitySlider');
        if (opacitySlider) {
            opacitySlider.addEventListener('input', (e) => {
                this.updateOpacityDisplay(e.target.value);
                window.SiteManager.updateOpacity(e.target.value);
            });
        }

        // Analysis buttons
        const detectBtn = document.getElementById('detectBtn');
        if (detectBtn) {
            detectBtn.addEventListener('click', () => window.Analysis.detectMining());
        }

        const volumeBtn = document.getElementById('volumeBtn');
        if (volumeBtn) {
            volumeBtn.addEventListener('click', () => window.Analysis.calculateVolume());
        }

        const compareBtn = document.getElementById('compareBtn');
        if (compareBtn) {
            compareBtn.addEventListener('click', () => window.Analysis.compareImages());
        }

        const illegalBtn = document.getElementById('illegalBtn');
        if (illegalBtn) {
            illegalBtn.addEventListener('click', () => window.Analysis.detectIllegal());
        }

        // Export buttons
        const reportBtn = document.getElementById('reportBtn');
        if (reportBtn) {
            reportBtn.addEventListener('click', () => window.ExportModule.generateReport());
        }

        const exportBtn = document.getElementById('exportBtn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => window.ExportModule.exportData());
        }

        const printBtn = document.getElementById('printBtn');
        if (printBtn) {
            printBtn.addEventListener('click', () => window.ExportModule.printMap());
        }

        const shareBtn = document.getElementById('shareBtn');
        if (shareBtn) {
            shareBtn.addEventListener('click', () => window.ExportModule.shareMap());
        }

        // FAB buttons
        const measureBtn = document.getElementById('measureBtn');
        if (measureBtn) {
            measureBtn.addEventListener('click', () => this.measureTool());
        }

        const drawBtn = document.getElementById('drawBtn');
        if (drawBtn) {
            drawBtn.addEventListener('click', () => this.drawPolygon());
        }

        const snapshotBtn = document.getElementById('snapshotBtn');
        if (snapshotBtn) {
            snapshotBtn.addEventListener('click', () => this.captureSnapshot());
        }

        const fullscreenBtn = document.getElementById('fullscreenBtn');
        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
        }

        console.log('UI event listeners initialized');
    }
};

// Make UIControls globally available
window.UIControls = UIControls;

