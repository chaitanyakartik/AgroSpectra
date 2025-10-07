
/* ==========================================
   FILE: js/utils/events.js
   Keyboard shortcuts and global events
   ========================================== */

const EventHandlers = {
    // Initialize keyboard shortcuts
    initKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case 's':
                        e.preventDefault();
                        window.ExportModule.exportData();
                        break;
                    case 'r':
                        e.preventDefault();
                        window.ExportModule.generateReport();
                        break;
                    case 'd':
                        e.preventDefault();
                        window.Analysis.detectMining();
                        break;
                    case 'f':
                        e.preventDefault();
                        window.UIControls.toggleFullscreen();
                        break;
                }
            }
        });

        console.log('Keyboard shortcuts enabled: Ctrl+S (Export), Ctrl+R (Report), Ctrl+D (Detect), Ctrl+F (Fullscreen)');
    }
};

// Make EventHandlers globally available
window.EventHandlers = EventHandlers;

