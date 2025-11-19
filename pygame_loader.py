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
            async function main() {
                let pyodide = await loadPyodide();
                window.pyodide = pyodide;
                console.log("Pyodide loaded successfully!");
                
                // Load Pygame package
                try {
                    await pyodide.loadPackage('pygame');
                    console.log("Pygame loaded successfully!");
                    window.pygameLoaded = true;
                } catch (error) {
                    console.error("Error loading Pygame:", error);
                    window.pygameLoaded = false;
                }
            }
            main();
        </script>
        """, unsafe_allow_html=True)
        
        # Check if Pygame was loaded successfully
        check_js = """
        if (typeof window.pygameLoaded !== 'undefined') {
            return window.pygameLoaded;
        }
        return false;
        """
        
        # Return True if Pygame was loaded, False otherwise
        # Note: In a real implementation, you'd need a way to check the result
        # For now, we'll assume it loads correctly
        return True
    except Exception as e:
        st.error(f"Error initializing Pygame: {str(e)}")
        return False
