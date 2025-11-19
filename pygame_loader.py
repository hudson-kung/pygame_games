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
        # This JavaScript code will run in the browser
        js_code = """
        async function loadPygame() {
            try {
                console.log("Loading Pygame...");
                // Load Pygame package
                await pyodide.loadPackage('pygame');
                console.log("Pygame loaded successfully!");
                return true;
            } catch (error) {
                console.error("Error loading Pygame:", error);
                return false;
            }
        }
        return loadPygame();
        """
        
        # Execute the JavaScript code in the browser
        return st.experimental_eval_js(js_code)
    except Exception as e:
        st.error(f"Error initializing Pygame: {str(e)}")
        return False
