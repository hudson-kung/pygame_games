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
import html                     # 🔤 For HTML escaping in code display
import time                     # ⏰ For the carousel timing
import pygame
# 🎨 PAGE CONFIGURATION
# This must be the first Streamlit command and only once per page
st.set_page_config(
    page_title="🎮 My Game Arcade",           # What shows in the browser tab
    page_icon="🎮",                            # The little icon in the tab
    layout="wide",                             # Use the full width of the screen
    initial_sidebar_state="collapsed"          # Start with sidebar hidden
)


# 💡 LEARNING MOMENT: Why do we import?
# Instead of writing ALL the code ourselves, we use code that other
# smart programmers already wrote! This is called "standing on the
# shoulders of giants" 🦸‍♀️


# ============================================================================
# SECTION 2: CONFIGURATION (Settings for Our Website)
# ============================================================================
# Let's set up some basic information about our website.
# These are like the "rules" of our game hosting platform!

# 🎨 PAGE CONFIGURATION (already set at the top)

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
        return "rgb(255, 0, 0)"  # Pure red for hard games! 🔴
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
            st.markdown(f"📊 **Difficulty:** <span style='color: {color}'>{game_info['difficulty']}</span>", unsafe_allow_html=True)
        
        # Buttons row
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            # Button to run the game
            if st.button(f"▶️ Play", key=f"play_{game_info['folder_name']}"):
                st.info(f"🎮 Starting {game_info['name']}...")
                run_pygame_game(game_info['path'])
        
        with col_btn2:
            # Button to view the code
            if st.button("📝 View Code", key=f"code_{game_info['folder_name']}", use_container_width=True):
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
    
    WHAT IT DOES: Shows the source code of a game with enhanced display
    
    INPUT: game_path (where the game folder is)
    OUTPUT: None (but displays code!)
    
    FILE I/O LESSON:
        We read the contents of a file and display it with nice formatting!
    """
    
    main_file = Path(game_path) / "main.py"
    
    if main_file.exists():
        try:
            with open(main_file, 'r') as file:
                code = file.read()  # Read all the text from the file
                
                st.markdown("### 🖥️ Game Source Code")
                
                # Create a full-width container with custom styling
                st.markdown("""
                <style>
                /* Make the code block take full width */
                .stCodeBlock {
                    width: 100% !important;
                    max-width: 100% !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }
                /* Style the code container */
                .stCodeBlock > div {
                    width: 100% !important;
                    max-width: 100% !important;
                }
                /* Style the pre element */
                .stCodeBlock pre {
                    width: 100% !important;
                    max-width: 100% !important;
                    height: 70vh !important;
                    margin: 0 !important;
                    padding: 20px !important;
                    background-color: white !important;
                    border: 1px solid #ddd !important;
                    border-radius: 8px !important;
                    overflow: auto !important;
                }
                /* Style the code */
                .stCodeBlock code {
                    font-size: 16px !important;
                    line-height: 1.6 !important;
                    width: 100% !important;
                    display: block !important;
                }
                /* Style line numbers */
                .stCodeBlock .linenumber {
                    min-width: 2.5em !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                # Display the code with syntax highlighting
                st.markdown('<div style="width: 100%;">', unsafe_allow_html=True)
                st.code(
                    code,
                    language='python',
                    line_numbers=True
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
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
    import streamlit as st
    
    # ========================================
    # CAROUSEL SECTION
    # ========================================
    st.markdown(
        """<style>
        .hero {
            position: relative;
            text-align: center;
            color: white;
        }
        .hero img {
            width: 100%;
            height: 80vh;
            object-fit: cover;
            filter: brightness(60%);
            border-radius: 10px;
        }
        .overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
        .button {
            background: linear-gradient(90deg, #9333ea, #ec4899);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 30px;
            cursor: pointer;
        }
        .button:hover {
            opacity: 0.9;
        }
        </style>""",
        unsafe_allow_html=True,
    )

    featured_games = [
        {
            "title": "Snake",
            "image": "https://coopboardgames.com/wp-content/uploads/2025/10/Google-Snake-Game.jpeg",
            "path": "./games/snake"
        },
        {
            "title": "Tetris",
            "image": "data:image/jpeg;base64,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",
            "path": "./games/tetris"
        },
        {
            "title": "Dodge The Zombies",
            "image": "https://vampire.survivors.wiki/images/thumb/Mad_Forest_gameplay.jpg/640px-Mad_Forest_gameplay.jpg?7fe12",
            "path": "./games/DTS"
        }
    ]

    # Initialize session state for carousel
    if 'carousel_index' not in st.session_state:
        st.session_state.carousel_index = 0
    if 'auto_play' not in st.session_state:
        st.session_state.auto_play = True
    if 'last_update' not in st.session_state:
        st.session_state.last_update = time.time()

    # Auto-advance carousel every 5 seconds
    current_time = time.time()
    if st.session_state.auto_play and (current_time - st.session_state.last_update) > 5:
        st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(featured_games)
        st.session_state.last_update = current_time
        st.rerun()

    # Get current game
    current_game = featured_games[st.session_state.carousel_index]


    
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
    import streamlit as st
import time

featured_games = [
    {
        "title": "Snake",
        "image": "https://coopboardgames.com/wp-content/uploads/2025/10/Google-Snake-Game.jpeg",
        "path": "./games/snake"
    },
    {
        "title": "Tetris",
        "image": "data:image/jpeg;base64,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",
        "path": "./games/tetris"
    },
    {
        "title": "Dodge The Zombies",
        "image": "https://vampire.survivors.wiki/images/thumb/Mad_Forest_gameplay.jpg/640px-Mad_Forest_gameplay.jpg?7fe12",
        "path": "./games/DTS"
    },
]

# Initialize session state for carousel
if 'carousel_index' not in st.session_state:
    st.session_state.carousel_index = 0
if 'auto_play' not in st.session_state:
    st.session_state.auto_play = True
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

st.set_page_config(page_title="Featured Games Carousel", layout="wide")
st.markdown(
    """<style>
    .hero {
        position: relative;
        text-align: center;
        color: white;
    }
    .hero img {
        width: 100%;
        height: 80vh;
        object-fit: cover;
        filter: brightness(60%);
        border-radius: 10px;
    }
    .overlay {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    .button {
        background: linear-gradient(90deg, #9333ea, #ec4899);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 18px;
        border-radius: 30px;
        cursor: pointer;
    }
        .button:hover {
            opacity: 0.9;
        }
    </style>""",
    unsafe_allow_html=True,
)

# Auto-advance carousel every 5 seconds
current_time = time.time()
if st.session_state.auto_play and (current_time - st.session_state.last_update) > 5:
    st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(featured_games)
    st.session_state.last_update = current_time
    st.rerun()

# Debug: Print the structure of featured_games
print("Featured Games Structure:", [game.keys() for game in featured_games])

# Get current game
current_game = featured_games[st.session_state.carousel_index]

# Ensure required keys exist
current_game.setdefault('path', '')
current_game.setdefault('title', 'Unknown Game')
current_game.setdefault('image', '')

# Display carousel
st.markdown(f"""
<div class='hero'>
    <img src='{current_game.get('image', '')}' alt='{current_game.get('title', 'Game')}' />
    <div class='overlay'>
        <h1 style='font-size: 60px; font-weight: bold; margin-bottom: 15px;'>Play {current_game.get('title', 'Game')}</h1>
        <p style='font-size: 20px; margin-bottom: 25px;'>Jump into action with our most popular featured games.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation and Play buttons
col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])

with col2:
    if st.button("⏮️ Previous", use_container_width=True):
        st.session_state.carousel_index = (st.session_state.carousel_index - 1) % len(featured_games)
        st.session_state.auto_play = False
        st.rerun()

with col3:
    if st.button("▶️ Play Now", type="primary", use_container_width=True):
        game_path = current_game.get('path')
        if not game_path:
            st.error("❌ This game doesn't have a valid path configured.")
        elif not os.path.exists(game_path):
            st.error(f"❌ Game not found at: {os.path.abspath(game_path)}")
            st.info(f"Current working directory: {os.getcwd()}")
        else:
            st.info(f"🎮 Launching {current_game.get('title', 'game')}...")
            try:
                run_pygame_game(game_path)
            except Exception as e:
                st.error(f"❌ Error launching game: {str(e)}")
        st.session_state.auto_play = False

with col4:
    if st.button("Next ⏭️", use_container_width=True):
        st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(featured_games)
        st.session_state.auto_play = False
        st.rerun()

# Indicator dots
dots = " ".join([f"{'🔵' if i == st.session_state.carousel_index else '⚪'}" for i in range(len(featured_games))])
st.markdown(f"<div style='text-align: center; margin-top: 20px;'>{dots}</div>", unsafe_allow_html=True)
    # ========================================
    # INSTRUCTIONS SECTION
    # ========================================
    
    # Create an expandable section (like an accordion)
    
        
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
                Made by Hudson using Python 🚀
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
            else:
                st.warning("No games found. Please add some games to the games folder.")


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
