
/* ==========================================
   FILE: js/main.js
   Application entry point - Ties everything together
   ========================================== */

const App = {
    // Initialize the application
    init() {
        console.log('%c⛏️ ORENEXUS Mining Monitor ', 
            'background: linear-gradient(135deg, #4CAF50, #8BC34A); color: white; font-size: 20px; padding: 10px 20px; border-radius: 5px;');
        
        try {
            // 1. Initialize map
            window.MapManager.init();
            
            // 2. Load mining sites
            window.SiteManager.init();
            
            // 3. Initialize UI controls and event listeners
            window.UIControls.initEventListeners();
            
            // 4. Initialize keyboard shortcuts
            window.EventHandlers.initKeyboardShortcuts();
            
            // 5. Update initial statistics
            window.Analysis.updateStats();
            
            // 6. Start real-time updates
            window.Analysis.startRealTimeUpdates();
            
            console.log('System initialized successfully');
            console.log('Keyboard shortcuts: Ctrl+S (Export), Ctrl+R (Report), Ctrl+D (Detect), Ctrl+F (Fullscreen)');
            
        } catch (error) {
            console.error('Failed to initialize application:', error);
            window.Helpers.notify('Failed to initialize application. Please refresh the page.', 'error');
        }
    }
};

// Start the application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => App.init());
} else {
    App.init();
}