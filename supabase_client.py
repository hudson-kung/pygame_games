import os
from typing import Optional, List, Dict, Any
from numpy.char import strip
from supabase import create_client, Client
import dotenv

#CRUD
#C — Create (add new data)
#R — Read (get or view data)
#U - Update (update existing data)
#D — Delete (remove data)s



def get_database() -> Optional[Client]:
    # Load environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    print("URL:", url)
    print("Key present:", bool(key))
    
    if not url or not key:
        print("Error: Missing Supabase URL or Key in environment variables")
        return None
        
    try:
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        return None

def add_game(name:str, description:str, author:str, difficulty:str = "medium", emoji:str = "🎮", folder_name:str = "")->bool :
    client = get_database()
   
   
    game_data = {
    
            "name": name.strip(),
            "description": description.strip(),
            "author": author.strip(),
            "difficulty": difficulty.strip(),
            "emoji": emoji.strip(),

    }
    client.table("games")

def get_games()-> List[Dict[str,Any]]:
    client = get_database()
    if not client:
        return []

    try:
        result = client.table("games").select("*").eq("is_active", True).execute()
        return result.data if result.data else []
    except:
        return []

def update_game(game_id: int, updates: Dict[str, Any])-> bool:
    client = get_database()
    if not client:
        return False

    try:
        result = client.table("games").update(updates).eq("id", game_id).execute()
        return bool(result.data)
    except:
        return False

def delete_game(game_id: int) -> bool:


    client = get_database()
    if not client:
        return False

    try:
        result = client.table("games").delete().eq("id", game_id).execute()
        return bool(result.data)
    except:
        return False

def increment_play_count(game_id: int) -> bool:
    client = get_database()
    if not client:
        return False

    try:
        result = client.table("games").select("play_count").eq("id", game_id).execute()
        if not result.data:
            return False

        current_count = result.data[0].get("play_count", 0)
        new_count = current_count + 1

        update_result = client.table("games").update({"play_count": new_count}).eq("id", game_id).execute()
        return bool(update_result.data)
    except:
        return False

def test_connection() -> bool:
    try:
        print("Attempting to connect to Supabase...")
        client = get_database()
        if not client:
            print("Failed to initialize Supabase client")
            return False

        print("Testing database connection...")
        # Try a simple query that should work with minimal permissions
        result = client.table('games').select("id").limit(1).execute()
        print("Successfully connected to Supabase!")
        print(f"Found {len(result.data) if result.data else 0} games")
        return True
    except Exception as e:
        print(f"Connection failed with error: {str(e)}")
        print("Please check:")
        print("1. Your internet connection")
        print("2. Supabase project URL and API key")
        print("3. Database permissions and table existence")
        return False

if __name__ == "__main__":
    if test_connection():
        print("Database connection successful.")

    else:
        print("Database connection unsuccessful.")