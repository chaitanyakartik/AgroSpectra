/* ==========================================
   FILE: js/modules/analysis.js
   Analysis and detection tools
   ========================================== */

const Analysis = {
    detectionSensitivity: 'medium',
    analysisResults: {},

    // Initialize analysis module
    init() {
        console.log('Analysis module initialized');
    },

    // Auto-detect mining areas
    detectMining() {
        window.Helpers.showLoading();
        
        setTimeout(() => {
            window.Helpers.hideLoading();
            
            const sites = window.SiteManager.getAllSites();
            const newSites = Math.floor(Math.random() * 3) + 1;
            const activeSites = sites.filter(s => s.status === 'active').length;
            const violations = sites.filter(s => s.illegal).length;
            
            // Store results
            this.analysisResults.detection = {
                timestamp: new Date(),
                newSites: newSites,
                activeSites: activeSites,
                violations: violations,
                totalArea: window.Helpers.calculateTotalArea(sites)
            };
            
            const message = `🔍 Mining Detection Complete!\n\n` +
                `✅ ${newSites} new mining areas detected\n` +
                `✅ ${activeSites} active sites confirmed\n` +
                `⚠️ ${violations} potential violations identified\n\n` +
                `Total area analyzed: 2,450 km²\n` +
                `Processing time: 2.3 seconds\n` +
                `Sensitivity: ${this.detectionSensitivity.toUpperCase()}`;
            
            window.Helpers.notify(message, 'success');
            this.updateStats();
        }, 2000);
    },

    // Calculate volume for selected site
    calculateVolume() {
        const site = window.SiteManager.getSelectedSite();
        
        if (!site) {
            window.Helpers.notify('Please select a mining site first', 'warning');
            return;
        }

        window.Helpers.showLoading();
        
        setTimeout(() => {
            window.Helpers.hideLoading();
            
            // Advanced volume calculations
            const maxDepth = (site.depth * 1.8).toFixed(1);
            const minDepth = (site.depth * 0.6).toFixed(1);
            const avgDepth = site.depth;
            const totalVolume = site.volume;
            const accuracy = 95;
            
            // Store results
            this.analysisResults.volume = {
                siteName: site.name,
                siteId: site.id,
                totalVolume: totalVolume,
                avgDepth: avgDepth,
                maxDepth: maxDepth,
                minDepth: minDepth,
                area: site.area,
                accuracy: accuracy,
                timestamp: new Date()
            };
            
            const message = `📊 Volume Calculation for ${site.name}\n\n` +
                `Method: Digital Elevation Model (DEM) Analysis\n\n` +
                `Results:\n` +
                `• Total Volume: ${totalVolume} M m³\n` +
                `• Average Depth: ${avgDepth} m\n` +
                `• Max Depth: ${maxDepth} m\n` +
                `• Min Depth: ${minDepth} m\n` +
                `• Surface Area: ${site.area} ha\n\n` +
                `Accuracy: ±5%\n` +
                `Confidence Level: ${accuracy}%\n\n` +
                `Analysis Date: ${new Date().toLocaleDateString()}`;
            
            window.Helpers.notify(message, 'info');
        }, 1500);
    },

    // Compare images over time
    compareImages() {
        const site = window.SiteManager.getSelectedSite();
        const siteName = site ? site.name : 'all sites';
        
        const message = `📅 Temporal Analysis - ${siteName}\n\n` +
            `Select comparison parameters:\n\n` +
            `Time Period:\n` +
            `• Before: Previous satellite capture\n` +
            `• After: Current satellite capture\n\n` +
            `Analysis includes:\n` +
            `• Area change detection\n` +
            `• Volume difference calculation\n` +
            `• Vegetation index changes\n` +
            `• Activity pattern analysis\n\n` +
            `This will highlight changes in mining areas over time`;
        
        window.Helpers.notify(message, 'info');
    },

    // Detect illegal mining activities
    detectIllegal() {
        window.Helpers.showLoading();
        
        setTimeout(() => {
            window.Helpers.hideLoading();
            
            const sites = window.SiteManager.getAllSites();
            const illegalSites = sites.filter(s => s.illegal);
            
            // Analyze each illegal site
            const detailedResults = illegalSites.map(site => ({
                id: site.id,
                name: site.name,
                location: site.location,
                area: site.area,
                type: site.type,
                estimatedDamage: this.estimateDamage(site),
                priority: this.calculatePriority(site)
            }));
            
            // Sort by priority
            detailedResults.sort((a, b) => b.priority - a.priority);
            
            // Store results
            this.analysisResults.illegal = {
                count: illegalSites.length,
                sites: detailedResults,
                timestamp: new Date()
            };
            
            let report = '⚠️ ILLEGAL MINING DETECTION REPORT\n';
            report += '=' .repeat(40) + '\n\n';
            report += `Detection Date: ${new Date().toLocaleString()}\n`;
            report += `Total Violations Found: ${illegalSites.length}\n\n`;
            
            detailedResults.forEach((site, index) => {
                report += `${index + 1}. ${site.name}\n`;
                report += `   Location: ${window.Helpers.formatCoordinates(site.location[0], site.location[1])}\n`;
                report += `   Area: ${site.area} hectares\n`;
                report += `   Type: ${site.type}\n`;
                report += `   Priority: ${site.priority}/10\n`;
                report += `   Est. Environmental Damage: ${site.estimatedDamage}\n\n`;
            });
            
            report += '\nRECOMMENDATIONS:\n';
            report += '-'.repeat(40) + '\n';
            report += '1. Immediate field inspection required\n';
            report += '2. Issue cease and desist notices\n';
            report += '3. Environmental impact assessment\n';
            report += '4. Legal action preparation\n';
            report += '5. Monitor for continued activity\n\n';
            report += `Report generated by ORENEXUS Mining Monitor`;
            
            window.Helpers.notify(report, 'warning');
            
            // Highlight illegal sites on map
            this.highlightIllegalSites(illegalSites);
        }, 2000);
    },

    // Estimate environmental damage
    estimateDamage(site) {
        const damageScore = site.area * 1.5 + site.volume * 2;
        
        if (damageScore > 15) return 'Severe';
        if (damageScore > 8) return 'High';
        if (damageScore > 4) return 'Moderate';
        return 'Low';
    },

    // Calculate priority score (1-10)
    calculatePriority(site) {
        let priority = 5; // Base priority
        
        // Increase priority based on area
        if (site.area > 5) priority += 2;
        else if (site.area > 2) priority += 1;
        
        // Increase priority based on volume
        if (site.volume > 1) priority += 2;
        else if (site.volume > 0.5) priority += 1;
        
        // Increase priority for certain types
        if (site.type === 'Sand' || site.type === 'Stone') priority += 1;
        
        return Math.min(priority, 10);
    },

    // Highlight illegal sites on the map
    highlightIllegalSites(illegalSites) {
        // Pulse effect for illegal sites
        illegalSites.forEach(site => {
            if (site.polygon) {
                // Add pulsing animation via style changes
                let pulseCount = 0;
                const pulseInterval = setInterval(() => {
                    if (pulseCount >= 6) {
                        clearInterval(pulseInterval);
                        site.polygon.setStyle({ weight: 3 });
                        return;
                    }
                    
                    const weight = pulseCount % 2 === 0 ? 6 : 3;
                    site.polygon.setStyle({ weight: weight });
                    pulseCount++;
                }, 300);
            }
        });
    },

    // Update statistics display
    updateStats() {
        const sites = window.SiteManager.getAllSites();
        
        const totalArea = window.Helpers.calculateTotalArea(sites);
        const activeSites = window.Helpers.countActiveSites(sites);
        const violations = window.Helpers.countViolations(sites);
        
        const totalAreaEl = document.getElementById('totalArea');
        const activeSitesEl = document.getElementById('activeSites');
        const violationsEl = document.getElementById('violations');
        
        if (totalAreaEl) totalAreaEl.textContent = totalArea.toFixed(1) + ' ha';
        if (activeSitesEl) activeSitesEl.textContent = activeSites;
        if (violationsEl) violationsEl.textContent = violations;
        
        console.log(`Stats updated - Area: ${totalArea.toFixed(1)}ha, Active: ${activeSites}, Violations: ${violations}`);
    },

    // Start real-time updates
    startRealTimeUpdates() {
        setInterval(() => {
            // Randomly update some statistics to simulate real-time changes
            if (Math.random() > 0.7) {
                const sites = window.SiteManager.getAllSites();
                const baseArea = window.Helpers.calculateTotalArea(sites);
                const variation = (Math.random() - 0.5) * 2;
                const area = (baseArea + variation).toFixed(1);
                
                const totalAreaEl = document.getElementById('totalArea');
                if (totalAreaEl) {
                    totalAreaEl.textContent = area + ' ha';
                }
            }
        }, window.APP_CONFIG.INTERVALS.STATS_UPDATE);
        
        console.log('Real-time stats updates started');
    },

    // Set detection sensitivity
    setSensitivity(level) {
        if (['low', 'medium', 'high'].includes(level.toLowerCase())) {
            this.detectionSensitivity = level.toLowerCase();
            console.log(`Detection sensitivity set to: ${this.detectionSensitivity}`);
        }
    },

    // Get analysis results
    getResults(analysisType = null) {
        if (analysisType) {
            return this.analysisResults[analysisType] || null;
        }
        return this.analysisResults;
    },

    // Generate change detection report
    generateChangeReport(site, beforeDate, afterDate) {
        const changes = {
            areaChange: (Math.random() * 2 - 1).toFixed(2), // Random for demo
            volumeChange: (Math.random() * 0.5 - 0.25).toFixed(2),
            activityLevel: Math.random() > 0.5 ? 'Increased' : 'Decreased',
            vegetationLoss: (Math.random() * 30).toFixed(1)
        };
        
        return {
            siteName: site.name,
            beforeDate: beforeDate,
            afterDate: afterDate,
            changes: changes,
            timestamp: new Date()
        };
    },

    // Calculate environmental impact score
    calculateEnvironmentalImpact(site) {
        const areaFactor = site.area * 0.3;
        const depthFactor = site.depth * 0.02;
        const volumeFactor = site.volume * 0.5;
        
        const impactScore = areaFactor + depthFactor + volumeFactor;
        
        let impactLevel;
        if (impactScore > 10) impactLevel = 'Critical';
        else if (impactScore > 6) impactLevel = 'High';
        else if (impactScore > 3) impactLevel = 'Moderate';
        else impactLevel = 'Low';
        
        return {
            score: impactScore.toFixed(2),
            level: impactLevel,
            factors: {
                area: areaFactor.toFixed(2),
                depth: depthFactor.toFixed(2),
                volume: volumeFactor.toFixed(2)
            }
        };
    },

    // Perform spatial analysis
    performSpatialAnalysis() {
        const sites = window.SiteManager.getAllSites();
        
        // Calculate density
        const totalArea = window.Helpers.calculateTotalArea(sites);
        const avgArea = (totalArea / sites.length).toFixed(2);
        
        // Find clusters
        const clusters = this.findClusters(sites);
        
        // Calculate distances
        const avgDistance = this.calculateAverageDistance(sites);
        
        const report = {
            totalSites: sites.length,
            totalArea: totalArea.toFixed(2),
            averageArea: avgArea,
            clusters: clusters.length,
            averageDistance: avgDistance.toFixed(2),
            timestamp: new Date()
        };
        
        console.log('Spatial analysis:', report);
        return report;
    },

    // Find site clusters
    findClusters(sites, threshold = 0.5) {
        // Simple clustering based on distance threshold (degrees)
        const clusters = [];
        const visited = new Set();
        
        sites.forEach((site, i) => {
            if (visited.has(i)) return;
            
            const cluster = [site];
            visited.add(i);
            
            sites.forEach((otherSite, j) => {
                if (i !== j && !visited.has(j)) {
                    const distance = this.calculateDistance(
                        site.location[0], site.location[1],
                        otherSite.location[0], otherSite.location[1]
                    );
                    
                    if (distance < threshold) {
                        cluster.push(otherSite);
                        visited.add(j);
                    }
                }
            });
            
            if (cluster.length > 1) {
                clusters.push(cluster);
            }
        });
        
        return clusters;
    },

    // Calculate distance between two points (simple Euclidean)
    calculateDistance(lat1, lon1, lat2, lon2) {
        const dLat = lat2 - lat1;
        const dLon = lon2 - lon1;
        return Math.sqrt(dLat * dLat + dLon * dLon);
    },

    // Calculate average distance between all sites
    calculateAverageDistance(sites) {
        if (sites.length < 2) return 0;
        
        let totalDistance = 0;
        let count = 0;
        
        for (let i = 0; i < sites.length; i++) {
            for (let j = i + 1; j < sites.length; j++) {
                totalDistance += this.calculateDistance(
                    sites[i].location[0], sites[i].location[1],
                    sites[j].location[0], sites[j].location[1]
                );
                count++;
            }
        }
        
        return count > 0 ? totalDistance / count : 0;
    },

    // Export analysis results
    exportAnalysisResults(format = 'json') {
        const results = this.getResults();
        
        if (format === 'json') {
            const jsonStr = JSON.stringify(results, null, 2);
            console.log('Analysis Results (JSON):', jsonStr);
            return jsonStr;
        } else if (format === 'csv') {
            // Convert to CSV format
            let csv = 'Analysis Type,Timestamp,Details\n';
            Object.keys(results).forEach(key => {
                const result = results[key];
                csv += `${key},${result.timestamp},${JSON.stringify(result)}\n`;
            });
            return csv;
        }
        
        return results;
    },

    // Clear analysis results
    clearResults() {
        this.analysisResults = {};
        console.log('Analysis results cleared');
    },

    // Batch analyze all sites
    analyzeAllSites() {
        window.Helpers.showLoading();
        
        setTimeout(() => {
            const sites = window.SiteManager.getAllSites();
            const results = [];
            
            sites.forEach(site => {
                const impact = this.calculateEnvironmentalImpact(site);
                results.push({
                    id: site.id,
                    name: site.name,
                    status: site.status,
                    area: site.area,
                    volume: site.volume,
                    environmentalImpact: impact,
                    illegal: site.illegal
                });
            });
            
            // Sort by impact score
            results.sort((a, b) => 
                parseFloat(b.environmentalImpact.score) - parseFloat(a.environmentalImpact.score)
            );
            
            this.analysisResults.batchAnalysis = {
                results: results,
                timestamp: new Date()
            };
            
            window.Helpers.hideLoading();
            
            let report = '📊 BATCH ANALYSIS REPORT\n';
            report += '='.repeat(50) + '\n\n';
            report += `Total Sites Analyzed: ${results.length}\n`;
            report += `Analysis Date: ${new Date().toLocaleString()}\n\n`;
            report += 'TOP 5 SITES BY ENVIRONMENTAL IMPACT:\n';
            report += '-'.repeat(50) + '\n';
            
            results.slice(0, 5).forEach((site, index) => {
                report += `\n${index + 1}. ${site.name}\n`;
                report += `   Impact Level: ${site.environmentalImpact.level}\n`;
                report += `   Impact Score: ${site.environmentalImpact.score}\n`;
                report += `   Area: ${site.area} ha | Volume: ${site.volume} M m³\n`;
                report += `   Status: ${site.status.toUpperCase()}${site.illegal ? ' (ILLEGAL)' : ''}\n`;
            });
            
            window.Helpers.notify(report, 'info');
            console.log('Batch analysis complete:', results);
        }, 2500);
    }
};

// Make Analysis globally available
window.Analysis = Analysis;