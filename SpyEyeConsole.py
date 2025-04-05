from pypresence import Presence
import win32gui
import json
import os
import sys
import win32process
import psutil
import time
import threading
import requests
from flask import Flask

# Wait for 30 seconds before starting the rest of the script
time.sleep(30)

IMAGE_MAP_FILE = 'image_map.json'

app = Flask(__name__)

# Path to the JSON file where we store the client ID
CLIENT_ID_FILE = 'client_id.json'
IMAGE_MAP_FILE = 'image_map.json'
DEFAULT_CLIENT_ID = '1314279361582596146'

def set_high_priority():
    p = psutil.Process(os.getpid())
    p.nice(psutil.HIGH_PRIORITY_CLASS)

def load_client_id():
    """
    Load the client ID from the JSON file or return the default client ID.
    """
    if os.path.exists(CLIENT_ID_FILE):
        with open(CLIENT_ID_FILE, 'r') as f:
            data = json.load(f)
            return data.get('client_id', DEFAULT_CLIENT_ID)
    return DEFAULT_CLIENT_ID

def save_client_id(client_id):
    """
    Save the client ID to the JSON file.
    """
    with open(CLIENT_ID_FILE, 'w') as f:
        json.dump({'client_id': client_id}, f)

def load_image_map():
    """
    Load the image map from the JSON file or return the default map.
    """
    if os.path.exists(IMAGE_MAP_FILE):
        with open(IMAGE_MAP_FILE, 'r') as f:
            return json.load(f)
    return {
    "msedge": "edge_icon",         # Edge Browser
    "chrome": "chrome_icon",       # Google Chrome
    "opera": "opera_icon",  # Opera Browser
    "brave": "brave_icon", # Brave Browser
    "firefox": "firefox_icon", #Firefox Browser
    "notepad": "notepad_icon",     # Notepad
    "google": "google_icon",  #Google
    "notepad++": "notepad_icon",  # Notepad++
    "discord": "discord_icon",     # Discord
    "explorer": "file_explorer_icon",  # File Explorer
    "spotify": "spotify_icon",     # Spotify
    "code": "vscode_icon",         # Visual Studio Code
    "slack": "slack_icon",         # Slack
    "microsoftstore": "store_icon",   # Microsoft Store
    "settings": "settings_icon",   # Settings
    "olk": "outlook_icon",     # Outlook
    "wmplayer": "media_player_icon",  # Windows Media Player
    "clipchamp": "clipchamp_icon", # Microsoft Clipchamp
    "xbox": "xbox_icon",           # Xbox App
    "steamwebhelper": "steam_icon",         # Steam
    "epicgameslauncher": "epicgames_icon", # Epic Games
    "upc": "ubisoft_icon",     # Ubisoft
    "searchhost": "search_icon", # Search
    "rockstargames": "rockstar_icon", # Rockstar Games
    "telegram": "telegram_icon",   # Telegram
    "nvidia app":"nvidia_app_icon", # NVIDIA
    "nvidia overlay":"nvidia_app_icon",  # nvidia overlay
    "calculator":"calculator_icon",  # Calculator
    "photos": "photos_icon",          # Photos
    "idle": "idle_icon",
    "youtube": "youtube_icon",      # YouTube
    "amazon music": "amazonmusic_icon", 
    "netplwiz": "netplwiz_icon",    # Netplwiz
    "taskmgr": "taskmgr_icon",
    "unknown": "default_icon"      # Default icon
    
    }

def save_image_map(image_map):
    """
    Save the image map to the JSON file.
    """
    with open(IMAGE_MAP_FILE, 'w') as f:
        json.dump(image_map, f, indent=4)

def get_client_id():
    """
    Get the client ID, use the default if not set.
    """
    return load_client_id()

app = Flask(__name__)

def extract_domain_name(window_title):
    """
    Extract the domain name from the window title if it is a YouTube URL.
    """
    if "youtube.com" in window_title.lower() or "youtube" in window_title.lower():
        return "YouTube"
    elif "google.com" in window_title.lower() or "google" in window_title.lower(): 
        return "Google"
    elif "reddit.com" in window_title.lower() or "reddit" in window_title.lower() or "r/" in window_title.lower(): 
        return "Reddit"
    elif "twitch.tv" in window_title.lower() or "twitch" in window_title.lower(): 
        return "twitch"
    elif "netflix.com" in window_title.lower() or "netflix" in window_title.lower(): 
        return "Netflix"
    return None

def get_active_window_details():
    """
    Get the active window title and the process name of the application.
    """
    try:
        # Get the active window handle
        window_handle = win32gui.GetForegroundWindow()

        # Get the process ID associated with the window
        _, process_id = win32process.GetWindowThreadProcessId(window_handle)

        # Get process name using psutil
        process_name = psutil.Process(process_id).name().lower()

        # Remove ".exe" from the process name (if present)
        process_name = process_name.replace(".exe", "")

        # Get active window title
        window_title = win32gui.GetWindowText(window_handle)

        return window_title, process_name
    except Exception as e:
        print(f"Error: {e}")
        return "Unknown Window", "unknown"

def is_game_running(process_name):
    """
    Check if the current process is a game by querying the Steam API.
    """
    try:
        # Example: Checking if the Steam client or any game is active
        if "steam" in process_name:
            # Get the current Steam user and check for active game (via Steam Web API)
            steam_user_id = "76561198972248415"  # Replace with actual Steam User ID
            response = requests.get(f'https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?steamid={steam_user_id}')
            
            if response.status_code == 200:
                data = response.json()
                if "game" in data:  # Check if a game is running
                    return True
                else:
                    return False
            else:
                print(f"Error: Steam API request failed with status {response.status_code}")
                return False
        else:
            # If it's not related to Steam, check known game processes
            game_processes = [
                "steam", "rockstargames", "ubisoft", "xbox", "wmplayer",
                "steamwebhelper", "gameoverlay", "origin", "battle.net"
            ]
            return any(game in process_name for game in game_processes)

    except Exception as e:
        print(f"Error checking if game is running: {e}")
        return False

def update_discord_rpc():
    """
    Continuously update Discord Rich Presence based on active window.
    """
    last_process = None  # Track the last active process
    last_window_title = None  # Track the last active window title
    last_active_time = time.time()  # Track the last time a window was active
    IDLE_THRESHOLD = 300  # Increase idle threshold to 300 seconds (5 minutes)
    
    while True:
        # Get the current active window and process
        active_window, process_name = get_active_window_details()
        
        # Initialize buttons variable
        buttons = [{"label": "By DAHAAHA", "url": "https://steamcommunity.com/id/thenameissubhan"}] # Default button with a valid URL

        # If no active window is detected, check if we've been idle
        if not active_window.strip():
            if time.time() - last_active_time > IDLE_THRESHOLD:
                # Set presence to IDLE if we've been inactive
                try:
                    rpc.update(
                        state="IDLE",
                        details="No active window",
                        large_image="idle_icon",
                        large_text="IDLE",
                        start=time.time(),
                        buttons=buttons # No buttons in IDLE state
                    )
                    print("Status: IDLE")
                except Exception as e:
                    print(f"Error setting IDLE status: {e}")
            time.sleep(0.3)  # Reduced sleep time to 0.4 seconds
            continue

        # If a game is running, disable custom RPC updates
        if is_game_running(process_name):
            try:
                rpc.clear()  # Clear the custom RPC if a game is running
                print("Game detected, Discord RPC is controlled by Discord.")
            except Exception as e:
                print(f"Error clearing Discord RPC: {e}")
            time.sleep(0.3)  # Reduced sleep time to 0.4 seconds
            continue

        # Check if the active process or window has changed
        if process_name != last_process or active_window != last_window_title:
            last_process = process_name
            last_window_title = active_window
            last_active_time = time.time()  # Reset the active timer

            # Extract domain name from active window title
            domain_name = extract_domain_name(active_window)
            
            # Load the image map from JSON
            image_map = load_image_map()

            if domain_name == "YouTube":
                state = f"Currently Watching | {active_window}"
                if len(state) > 128:
                    state = state[:128 - len("... | **YouTube** |")]
                image_key = "youtube_icon"
                # Ensure state is within the limit
                state = state[:128]
            elif domain_name =="Google":
                state = f"Active on |{active_window}"
                image_key = "google_icon"
                # Ensure state is within the limit
                state = state[:128]
            elif domain_name =="twitch":
                state = f"Currently Watching | {active_window}"
                image_key = "twitch_icon"
                # Ensure state is within the limit
                state = state[:128]
            elif domain_name =="Reddit":
                state = f"Active on | {active_window}"
                image_key = "reddit_icon"               
                # Ensure state is within the limit
                state = state[:128]
            elif domain_name =="Netflix":
                state = f"Watching Now | {active_window}"
                image_key = "netflix_icon"               
                # Ensure state is within the limit
                state = state[:128]
            elif process_name == "unknown":
                state = f"Active on {active_window}"
                image_key = "unknown_icon"
            else:
                # Use original state format
                state = f"Active on | {active_window[:128]}"  # Limit to 128 characters
                state = state[:128]  # Ensure state is within the limit
                image_key = image_map.get(process_name, "default_icon")

            # Update Discord Rich Presence with current details
            try:
                rpc.update(
                    state=state,
                    details=f"Using {process_name.capitalize()}",
                    large_image=image_key,
                    large_text=process_name.capitalize(),
                    start=time.time(),
                    buttons=buttons
                )
                print(f"Window Title: {active_window}")
                print(f"Process Name: {process_name}")
                print(f"State: {state}")  # Debug print
            except Exception as e:
                print(f"Error updating Discord RPC: {e}")

        # Sleep to prevent constant high CPU usage
        time.sleep(0.4)  # Reduced sleep time to 0.4 seconds
        
def add_image_map(new_key, new_value):
    """
    Add a new entry to the image map.
    """
    # Load the image map from the JSON file
    image_map = load_image_map()

    # Check if the key already exists
    if new_key in image_map:
        print(f"Error: Key '{new_key}' already exists in the image map.")
        return

    # Add the new entry before the "default_icon"
    image_map = {key: value for key, value in image_map.items() if key != "default_icon"}
    image_map[new_key] = new_value
    image_map["default_icon"] = "default_icon"

    # Save the updated image map to the JSON file
    save_image_map(image_map)

    print(f"Image map entry '{new_key}: {new_value}' added successfully.")

# Main script starts here
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '--update-client-id':
            if len(sys.argv) > 2:
                new_client_id = sys.argv[2]
                save_client_id(new_client_id)
                print("Client ID updated successfully.")
            else:
                print("Error: No client ID provided. Usage: finall.exe --update-client-id <new_client_id>")
            sys.exit(0)
        elif sys.argv[1] == '--add-image-map':
            if len(sys.argv) > 3:
                new_key = sys.argv[2]
                new_value = sys.argv[3]
                add_image_map(new_key, new_value)
            else:
                print("Error: Incorrect usage. Usage: finall.exe --add-image-map <new_key> <new_value>")
            sys.exit(0)
    
    client_id = get_client_id()
    set_high_priority()  # Set process to high priority
    rpc = Presence(client_id)
    try:
        rpc.connect()
        print("RPC connected successfully.")
    except Exception as e:
        print(f"Error connecting RPC: {e}")

    # Run the Flask app and Discord RPC update in parallel using threads
    threading.Thread(target=update_discord_rpc, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)