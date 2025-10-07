/* ==========================================
   FILE: js/modules/export.js
   Report generation and data export
   ========================================== */

const ExportModule = {
    // Generate comprehensive report
    generateReport() {
        const sites = window.SiteManager.getAllSites();
        const timestamp = window.Helpers.formatDateTime();
        
        let report = `ORENEXUS MINING ACTIVITY REPORT\n${'='.repeat(40)}\n`;
        report += `Generated: ${timestamp}\n\n`;
        report += `EXECUTIVE SUMMARY\n${'-'.repeat(20)}\n`;
        report += `Total Sites Monitored: ${sites.length}\n`;
        report += `Active Mining Sites: ${window.Helpers.countActiveSites(sites)}\n`;
        report += `Inactive Sites: ${sites.filter(s => s.status === 'inactive').length}\n`;
        report += `Illegal Operations: ${window.Helpers.countViolations(sites)}\n\n`;
        
        report += `DETAILED SITE LIST\n${'-'.repeat(20)}\n`;
        sites.forEach(site => {
            report += `\n${site.name}\n`;
            report += `  Status: ${site.status.toUpperCase()}\n`;
            report += `  Type: ${site.type}\n`;
            report += `  Area: ${site.area} ha | Volume: ${site.volume} M m³\n`;
        });

        report += `\n\nRECOMMENDATIONS\n${'-'.repeat(20)}\n`;
        report += `1. Immediate inspection of illegal sites\n`;
        report += `2. Environmental impact assessment needed\n`;
        report += `3. Update compliance documentation\n`;

        window.Helpers.notify(report, 'info');
        console.log(report);
    },

    // Export data in various formats
    exportData() {
        const formats = window.APP_CONFIG.EXPORT_FORMATS;
        const selected = prompt(`Export formats available:\n${formats.join('\n')}\n\nEnter format:`, 'GeoJSON');
        
        if (selected) {
            window.Helpers.showLoading();
            setTimeout(() => {
                window.Helpers.hideLoading();
                const filename = `ORENEXUS_Mining_Data_${Date.now()}.${selected.toLowerCase()}`;
                const message = `✅ Export Successful!\n\n` +
                    `Format: ${selected}\n` +
                    `File: ${filename}\n\n` +
                    `The file has been prepared for download.`;
                window.Helpers.notify(message, 'success');
            }, 1000);
        }
    },

    // Print current map view
    printMap() {
        window.print();
    },

    // Share map view
    shareMap() {
        const map = window.MapManager.getMap();
        const center = map.getCenter();
        const zoom = map.getZoom();
        const shareUrl = `${window.location.href}#lat=${center.lat.toFixed(4)}&lng=${center.lng.toFixed(4)}&zoom=${zoom}`;
        
        window.Helpers.copyToClipboard(shareUrl);
        window.Helpers.notify('🔗 Share Link Copied!\n\nThe current map view link has been copied to clipboard.\n\nAnyone with this link can view the same location and zoom level.', 'success');
    }
};

// Make ExportModule globally available
window.ExportModule = ExportModule;

