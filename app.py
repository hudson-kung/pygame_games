"""
🎮 STREAMLIT PYGAME GAME HOSTING WEBSITE 🎮

Welcome to your coding tutorial! This file is organized into sections.
Read each section carefully - the comments will teach you:
- How to structure data (data structures!)
- How to build a website layout
- How Python code works
- How to organize a real project

TIME TO READ: About 30-45 minutes
TIME TO EXPERIMENT: Another 30 minutes
TOTAL FUN: 100%! 🎉

Let's start coding!
"""

# ============================================================================
# SECTION 1: IMPORTS (Loading Our Tools)
# ============================================================================
# Think of imports like opening your toolbox before building something.
# Each import gives us special powers!

import streamlit as st          # 🌟 Makes beautiful websites easily!
import os                       # 📁 Helps us work with files and folders
import json                     # 📊 Reads/writes JSON data (like game configs)
from pathlib import Path        # 🛤️ A modern way to handle file paths
import subprocess               # 🚀 Can run other programs (like Pygame games)

# 💡 LEARNING MOMENT: Why do we import?
# Instead of writing ALL the code ourselves, we use code that other
# smart programmers already wrote! This is called "standing on the
# shoulders of giants" 🦸‍♀️


# ============================================================================
# SECTION 2: CONFIGURATION (Settings for Our Website)
# ============================================================================
# Let's set up some basic information about our website.
# These are like the "rules" of our game hosting platform!

# 🎨 PAGE CONFIGURATION
# This makes our website look professional from the start!
st.set_page_config(
    page_title="🎮 My Game Arcade",           # What shows in the browser tab
    page_icon="🎮",                            # The little icon in the tab
    layout="wide",                             # Use the full width of the screen
    initial_sidebar_state="collapsed"          # Start with sidebar hidden
)

# 📂 DIRECTORY CONFIGURATION
# This is a DATA STRUCTURE! We're using a dictionary to store settings.
# Dictionaries have KEYS (like "games_dir") and VALUES (like "./games")

CONFIG = {
    "games_dir": "./games",                    # Where all game folders live
    "default_emoji": "🎮",                     # If a game doesn't have an emoji
    "items_per_row": 3                         # How many game cards per row
}

# 💡 LEARNING MOMENT: What's a dictionary?
# A dictionary is like a real dictionary - you look up a WORD (key) 
# to find its DEFINITION (value).
# Example: CONFIG["games_dir"] gives us "./games"


# ============================================================================
# SECTION 3: HELPER FUNCTIONS (Our Mini Tools)
# ============================================================================
# Functions are like recipes - they do specific tasks!
# We write them once, use them many times. This is called "reusability" ♻️

def load_game_config(game_folder_path):
    """
    📖 FUNCTION: load_game_config
    
    WHAT IT DOES: Reads a game's config.json file and gives us the data
    
    INPUT (Parameter):
        - game_folder_path: The folder where a game lives (ex: "./games/snake")
    
    OUTPUT (Return value):
        - A dictionary with game info (name, author, description, etc.)
        - OR None if there's no config file
    
    DATA STRUCTURE LESSON:
        We return a DICTIONARY (also called a "dict" or "object")
        Dictionaries store related information together!
    """
    
    # First, let's build the path to the config.json file
    # Path() is like giving the computer GPS directions to a file!
    config_path = Path(game_folder_path) / "config.json"
    
    # Check if the config file actually exists
    # (It's good to check before trying to open files!)
    if not config_path.exists():
        return None  # Return None means "sorry, couldn't find it!"
    
    # Now let's try to read the file
    # We use "try/except" to handle errors gracefully
    try:
        with open(config_path, 'r') as file:
            # 💡 "with open" automatically closes the file when we're done
            # This is good practice - like closing the fridge door!
            
            config_data = json.load(file)  # json.load converts JSON text to a dictionary
            return config_data
            
    except Exception as e:
        # If something goes wrong, print an error message
        print(f"❌ Error loading config for {game_folder_path}: {e}")
        return None


def get_all_games():
    """
    📖 FUNCTION: get_all_games
    
    WHAT IT DOES: Finds ALL game folders and gets their information
    
    INPUT: None (we use the CONFIG dictionary from above!)
    
    OUTPUT: A LIST of dictionaries (one dictionary per game)
    
    DATA STRUCTURE LESSON:
        This returns a LIST of DICTIONARIES!
        - LIST: An ordered collection [item1, item2, item3]
        - Each item is a DICTIONARY with game info
        
        Example result:
        [
            {"name": "Snake", "author": "You", "path": "./games/snake"},
            {"name": "Tetris", "author": "You", "path": "./games/tetris"}
        ]
    """
    
    games = []  # Start with an empty list - we'll add games to it!
    
    # Get the games directory path
    games_dir = Path(CONFIG["games_dir"])
    
    # Check if the games folder exists
    if not games_dir.exists():
        st.error(f"❌ Games directory '{CONFIG['games_dir']}' not found!")
        return []  # Return empty list if no games folder
    
    # Loop through each item in the games folder
    # iterdir() gives us everything in a folder
    for item in games_dir.iterdir():
        
        # We only want folders, not random files
        if item.is_dir():  # is_dir() checks "is this a directory/folder?"
            
            # Load the game's configuration
            config = load_game_config(item)
            
            # Create a dictionary with all the game info
            game_info = {
                "folder_name": item.name,                                   # Ex: "snake"
                "path": str(item),                                          # Ex: "./games/snake"
                "name": config.get("name", item.name) if config else item.name,  # Game name
                "description": config.get("description", "No description") if config else "No description",
                "author": config.get("author", "Unknown") if config else "Unknown",
                "difficulty": config.get("difficulty", "Medium") if config else "Medium",
                "emoji": config.get("emoji", CONFIG["default_emoji"]) if config else CONFIG["default_emoji"]
            }
            
            # 💡 LEARNING MOMENT: What's .get()?
            # config.get("name", "Default") means:
            # "Try to get 'name', but if it doesn't exist, use 'Default' instead"
            # This prevents errors if a key is missing!
            
            # Add this game to our list
            games.append(game_info)  # append() adds an item to the end of a list
    
    return games  # Give back the complete list of games!


def get_difficulty_color(difficulty):
    """
    📖 FUNCTION: get_difficulty_color
    
    WHAT IT DOES: Gives each difficulty level a color!
    
    INPUT: difficulty (a string like "Easy", "Medium", or "Hard")
    OUTPUT: A color name (string)
    
    CONTROL FLOW LESSON:
        We use IF/ELIF/ELSE to make decisions!
        The computer checks each condition in order.
    """
    
    if difficulty.lower() == "easy":
        return "green"      # Green means go! Easy games! 🟢
    elif difficulty.lower() == "medium":
        return "orange"     # Orange means careful! Medium difficulty! 🟠
    elif difficulty.lower() == "hard":
        return "red"        # Red means danger! Hard games! 🔴
    else:
        return "blue"       # Blue for anything else! 🔵


def create_game_card(game_info):
    """
    📖 FUNCTION: create_game_card
    
    WHAT IT DOES: Creates a beautiful display card for one game
    
    INPUT: game_info (a dictionary with game data)
    OUTPUT: None (but it displays stuff on the screen!)
    
    UI/LAYOUT LESSON:
        This function builds the visual layout for a game.
        Think of it like designing a trading card! 🎴
    """
    
    # Get the difficulty color
    color = get_difficulty_color(game_info["difficulty"])
    
    # Create a container (like a box) for this game card
    with st.container():
        
        # Add a colored border using HTML/CSS
        # st.markdown lets us use HTML for fancy styling!
        st.markdown(
            f"""
            <div style="
                padding: 20px;
                border-radius: 10px;
                border: 3px solid {color};
                background-color: rgba(255, 255, 255, 0.05);
                margin-bottom: 20px;
            ">
            """,
            unsafe_allow_html=True
        )
        
        # Game title with emoji
        st.subheader(f"{game_info['emoji']} {game_info['name']}")
        
        # Game description
        st.write(game_info['description'])
        
        # Create two columns for metadata
        # Columns let us put things side-by-side!
        col1, col2 = st.columns(2)
        
        with col1:
            st.caption(f"👤 **Author:** {game_info['author']}")
        
        with col2:
            st.caption(f"📊 **Difficulty:** :{color}[{game_info['difficulty']}]")
        
        # Buttons row
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            # Button to run the game
            if st.button(f"▶️ Play", key=f"play_{game_info['folder_name']}"):
                st.info(f"🎮 Starting {game_info['name']}...")
                run_pygame_game(game_info['path'])
        
        with col_btn2:
            # Button to view the code
            if st.button(f"📝 View Code", key=f"code_{game_info['folder_name']}"):
                show_game_code(game_info['path'])
        
        # Close the HTML div
        st.markdown("</div>", unsafe_allow_html=True)


def run_pygame_game(game_path):
    """
    📖 FUNCTION: run_pygame_game
    
    WHAT IT DOES: Launches a Pygame game in a new window
    
    INPUT: game_path (where the game folder is)
    OUTPUT: None (but starts a game!)
    
    PROCESS LESSON:
        subprocess.Popen starts a new program
        It's like double-clicking an app!
    """
    
    main_file = Path(game_path) / "main.py"
    
    if main_file.exists():
        try:
            # subprocess.Popen runs a command
            # We're running: python3 main.py
            subprocess.Popen(["python3", str(main_file)])
            st.success("✅ Game launched! Check your other windows!")
        except Exception as e:
            st.error(f"❌ Error launching game: {e}")
    else:
        st.error(f"❌ Could not find main.py in {game_path}")


def show_game_code(game_path):
    """
    📖 FUNCTION: show_game_code
    
    WHAT IT DOES: Shows the source code of a game
    
    INPUT: game_path (where the game folder is)
    OUTPUT: None (but displays code!)
    
    FILE I/O LESSON:
        We read the contents of a file and display it!
    """
    
    main_file = Path(game_path) / "main.py"
    
    if main_file.exists():
        try:
            with open(main_file, 'r') as file:
                code = file.read()  # Read all the text from the file
                
                # Display code with syntax highlighting
                st.code(code, language='python')
        except Exception as e:
            st.error(f"❌ Error reading code: {e}")
    else:
        st.error(f"❌ Could not find main.py in {game_path}")


# ============================================================================
# SECTION 4: MAIN APP LAYOUT (Building the Website)
# ============================================================================
# This is where we put everything together!
# Think of this as building with LEGO blocks - we stack components! 🧱

def main():
    """
    📖 FUNCTION: main
    
    WHAT IT DOES: The main function that builds our entire website!
    
    LAYOUT LESSON:
        Websites are built from top to bottom, just like reading a book!
        Each st.something() call adds a new element to the page.
    """
    
    # ========================================
    # HEADER SECTION
    # ========================================
    
    # Main title - centered and big!
    st.markdown(
        """
        <h1 style='text-align: center; color: #FF6B6B;'>
            🎮 My Python Game Arcade 🎮
        </h1>
        """,
        unsafe_allow_html=True
    )
    
    # Subtitle
    st.markdown(
        """
        <p style='text-align: center; font-size: 20px;'>
            Welcome to your personal game hosting website! 🚀
        </p>
        """,
        unsafe_allow_html=True
    )
    
    # Add some space
    st.markdown("---")  # This creates a horizontal line
    
    # ========================================
    # INSTRUCTIONS SECTION
    # ========================================
    
    # Create an expandable section (like an accordion)
    with st.expander("📚 How to Add Your Own Games (Click to expand!)"):
        st.markdown("""
        ### Adding a new game is super easy! Just follow these steps:
        
        1. **Create a folder** in the `games/` directory:
           ```
           games/my-awesome-game/
           ```
        
        2. **Add your game file** - MUST be named `main.py`:
           ```
           games/my-awesome-game/main.py
           ```
        
        3. **Create a config file** with your game info:
           ```json
           {
             "name": "My Awesome Game",
             "description": "A super fun game about...",
             "author": "Your Name",
             "difficulty": "Easy",
             "emoji": "🎯"
           }
           ```
           Save this as `games/my-awesome-game/config.json`
        
        4. **Refresh this page** - your game will appear automatically! 🎉
        
        **That's it!** The website automatically finds all games in the `games/` folder!
        """)
    
    st.markdown("---")
    
    # ========================================
    # GAMES SECTION
    # ========================================
    
    # Get all available games using our helper function!
    games = get_all_games()
    
    # Show statistics
    st.subheader(f"🎯 Available Games: {len(games)}")
    
    # 💡 LEARNING MOMENT: len() gives us the length of a list
    # If games = [game1, game2, game3], then len(games) = 3
    
    if len(games) == 0:
        # If no games found, show a helpful message
        st.warning("""
        📭 No games found yet! 
        
        Add some games to the `games/` folder to get started!
        Check the instructions above ☝️
        """)
    else:
        # We have games! Let's display them in a grid!
        
        # LAYOUT MAGIC: Create a grid with multiple columns
        # We'll put 3 games per row (you can change this!)
        
        items_per_row = CONFIG["items_per_row"]
        
        # 💡 LEARNING MOMENT: We're going to use a loop to create rows!
        # range(start, stop, step) creates numbers
        # Example: range(0, 9, 3) gives us 0, 3, 6
        
        for i in range(0, len(games), items_per_row):
            # Create columns for this row
            cols = st.columns(items_per_row)
            
            # Fill each column with a game card
            for col_idx in range(items_per_row):
                game_idx = i + col_idx
                
                # Make sure we don't go past the end of our games list!
                if game_idx < len(games):
                    with cols[col_idx]:
                        create_game_card(games[game_idx])
    
    # ========================================
    # FOOTER SECTION
    # ========================================
    
    st.markdown("---")
    
    st.markdown(
        """
        <p style='text-align: center; color: gray;'>
            Made with ❤️ using Streamlit and Python<br>
            🎮 Keep coding, keep creating, keep having fun! 🚀
        </p>
        """,
        unsafe_allow_html=True
    )
    
    # ========================================
    # SIDEBAR (Optional Extra Info)
    # ========================================
    
    with st.sidebar:
        st.title("🎨 Game Filters")
        st.info("Coming soon: Filter games by difficulty, author, and more!")
        
        st.markdown("---")
        
        st.title("📊 Statistics")
        
        if len(games) > 0:
            # Count games by difficulty
            # This uses a DATA STRUCTURE technique called "counting"!
            
            difficulty_counts = {}  # Empty dictionary to store counts
            
            for game in games:
                diff = game['difficulty']
                if diff in difficulty_counts:
                    difficulty_counts[diff] += 1  # Add 1 to existing count
                else:
                    difficulty_counts[diff] = 1    # Start counting this difficulty
            
            # Display the counts
            st.write("**Games by Difficulty:**")
            for diff, count in difficulty_counts.items():
                st.write(f"{diff}: {count}")


# ============================================================================
# SECTION 5: RUN THE APP!
# ============================================================================
# This is the "start button" of our program!

if __name__ == "__main__":
    # 💡 LEARNING MOMENT: What does this mean?
    # __name__ == "__main__" checks if this file is being run directly
    # (not imported by another file)
    # 
    # It's like saying: "If someone clicks me to run, do the main() function!"
    
    main()  # Start the app!


# ============================================================================
# 🎉 CONGRATULATIONS! 🎉
# ============================================================================
# You've just read through a complete Streamlit web application!
# 
# Here's what you learned:
# ✅ Data structures (lists, dictionaries)
# ✅ Functions and how to organize code
# ✅ File I/O (reading files)
# ✅ Control flow (if/else statements, loops)
# ✅ Web layout (columns, containers, cards)
# ✅ User interface design
# 
# NEXT STEPS:
# 1. Run this app: streamlit run app.py
# 2. Try modifying the code - change colors, text, layout!
# 3. Add your own games!
# 4. Deploy to Streamlit Cloud!
# 
# Keep experimenting and have fun! 🚀
# ============================================================================
