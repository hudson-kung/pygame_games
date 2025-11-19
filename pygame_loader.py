"""
Pygame loader for Streamlit with Pyodide
This module handles loading Pygame in the browser environment.
"""
import streamlit as st

def load_pygame():
    """
    Load Pygame using Pyodide in the browser.
    Returns True if successful, False otherwise.
    """
    try:
        # Add Pyodide initialization if not already loaded
        st.markdown("""
        <script src="https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js"></script>
        <script>
            window.pyodideReady = false;
            window.pygameLoaded = false;
            
            async function initializePyodide() {
                try {
                    console.log("Initializing Pyodide...");
                    let pyodide = await loadPyodide({
                        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.23.4/full/"
                    });
                    window.pyodide = pyodide;
                    
                    // Set up the canvas for Pygame
                    const canvas = document.createElement('canvas');
                    canvas.id = 'pygame-canvas';
                    canvas.width = 800;
                    canvas.height = 600;
                    canvas.style.border = '2px solid #ccc';
                    canvas.style.display = 'block';
                    canvas.style.margin = '10px auto';
                    
                    // Store canvas reference
                    window.pygameCanvas = canvas;
                    
                    // Load Pygame package
                    console.log("Loading Pygame package...");
                    await pyodide.loadPackage(['pygame', 'numpy']);
                    
                    // Initialize Pygame with the canvas
                    await pyodide.runPythonAsync(`
                        import pygame
                        import js
                        import numpy as np
                        
                        # Initialize Pygame for web
                        pygame.init()
                        pygame.display.init()
                        
                        # Set up the display surface
                        screen = pygame.display.set_mode((800, 600))
                        pygame.display.set_caption("Pygame in Browser")
                        
                        print("Pygame initialized successfully!")
                    `);
                    
                    window.pygameLoaded = true;
                    window.pyodideReady = true;
                    console.log("Pygame loaded and initialized successfully!");
                    
                    // Dispatch event to notify that Pygame is ready
                    window.dispatchEvent(new Event('pygameReady'));
                    
                } catch (error) {
                    console.error("Error initializing Pyodide/Pygame:", error);
                    window.pyodideReady = true;
                    window.pygameLoaded = false;
                }
            }
            
            // Start initialization
            initializePyodide();
        </script>
        """, unsafe_allow_html=True)
        
        # Add a status indicator
        st.markdown("""
        <div id="pygame-status" style="padding: 10px; background: #f0f0f0; border-radius: 5px; margin: 10px 0;">
            <p>🎮 Initializing Pygame in browser...</p>
        </div>
        
        <script>
            // Update status when Pygame is ready
            window.addEventListener('pygameReady', function() {
                const status = document.getElementById('pygame-status');
                if (window.pygameLoaded) {
                    status.innerHTML = '<p style="color: green;">✅ Pygame is ready! Games can now be played.</p>';
                } else {
                    status.innerHTML = '<p style="color: red;">❌ Failed to load Pygame. Please refresh the page.</p>';
                }
            });
        </script>
        """, unsafe_allow_html=True)
        
        return True
    except Exception as e:
        st.error(f"Error initializing Pygame: {str(e)}")
        return False
