from pypresence import Presence
import win32gui
import win32process
import psutil
import time
import json
import os
import sys
import win32api

# Wait for 30 seconds before starting the rest of the script
time.sleep(30)

# Constants
CLIENT_ID_FILE = 'client_id.json'
IMAGE_MAP_FILE = 'image_map.json'
DEFAULT_CLIENT_ID = '1314279361582596146'
IDLE_THRESHOLD = 300  # 5 minutes in seconds

# Default image map
DEFAULT_IMAGE_MAP = {
    "msedge": "edge_icon",
    "chrome": "chrome_icon",
    "opera": "opera_icon",
    "brave": "brave_icon",
    "firefox": "firefox_icon",
    "notepad": "notepad_icon",
    "google": "google_icon",
    "notepad++": "notepad_icon",
    "discord": "discord_icon",
    "explorer": "file_explorer_icon",
    "spotify": "spotify_icon",
    "code": "vscode_icon",
    "slack": "slack_icon",
    "microsoftstore": "store_icon",
    "settings": "settings_icon",
    "olk": "outlook_icon",
    "wmplayer": "media_player_icon",
    "clipchamp": "clipchamp_icon",
    "xbox": "xbox_icon",
    "steamwebhelper": "steam_icon",
    "epicgameslauncher": "epicgames_icon",
    "upc": "ubisoft_icon",
    "searchhost": "search_icon",
    "rockstargames": "rockstar_icon",
    "telegram": "telegram_icon",
    "nvidia app": "nvidia_app_icon",
    "copilot": "copilot_icon",
    "nvidia overlay": "nvidia_app_icon",
    "calculator": "calculator_icon",
    "photos": "photos_icon",
    "idle": "idle_icon",
    "youtube": "youtube_icon",
    "amazon music": "amazonmusic_icon",
    "netplwiz": "netplwiz_icon",
    "taskmgr": "taskmgr_icon",
    "unknown": "default_icon"
}

def set_high_priority():
    """Set the script process to high priority."""
    p = psutil.Process(os.getpid())
    p.nice(psutil.HIGH_PRIORITY_CLASS)

def load_client_id():
    """Load the Discord client ID from a JSON file or return the default."""
    if os.path.exists(CLIENT_ID_FILE):
        with open(CLIENT_ID_FILE, 'r') as f:
            data = json.load(f)
            return data.get('client_id', DEFAULT_CLIENT_ID)
    return DEFAULT_CLIENT_ID

def save_client_id(client_id):
    """Save a new client ID to the JSON file."""
    with open(CLIENT_ID_FILE, 'w') as f:
        json.dump({'client_id': client_id}, f)

def load_image_map():
    """Load the image map from a JSON file or return the default."""
    if os.path.exists(IMAGE_MAP_FILE):
        with open(IMAGE_MAP_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_IMAGE_MAP

def save_image_map(image_map):
    """Save the updated image map to the JSON file."""
    with open(IMAGE_MAP_FILE, 'w') as f:
        json.dump(image_map, f, indent=4)

def get_client_id():
    """Retrieve the current client ID."""
    return load_client_id()

def get_idle_time():
    """Calculate the time since last user input in seconds."""
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0

def extract_domain_name(window_title):
    """
    Extract the domain name from the window title if it is a YouTube URL.
    """
    if "youtube.com" in window_title.lower() or "youtube" in window_title.lower():
        return "YouTube"
    elif "gmail.com" in window_title.lower() or "gmail" in window_title.lower(): 
        return "Gmail"
    elif "reddit.com" in window_title.lower() or "reddit" in window_title.lower() or "r/" in window_title.lower(): 
        return "Reddit"
    elif "twitch.tv" in window_title.lower() or "twitch" in window_title.lower(): 
        return "twitch"   
    elif "netflix.com" in window_title.lower() or "netflix" in window_title.lower(): 
        return "Netflix"
    return None

def get_active_window_details():
    """Get the title and process name of the active window."""
    try:
        window_handle = win32gui.GetForegroundWindow()
        if not window_handle:
            return "Unknown Window", "unknown"
        _, process_id = win32process.GetWindowThreadProcessId(window_handle)
        process = psutil.Process(process_id)
        process_name = process.name().lower().replace(".exe", "")
        window_title = win32gui.GetWindowText(window_handle) or "Untitled"
        return window_title, process_name
    except (psutil.NoSuchProcess, Exception) as e:
        print(f"Error getting window details: {e}")
        return "Unknown Window", "unknown"


def update_discord_rpc():
    """Main loop to update Discord Rich Presence based on user activity."""
    client_id = get_client_id()
    rpc = Presence(client_id)
    try:
        rpc.connect()
        print("RPC connected successfully.")
    except Exception as e:
        print(f"Error connecting RPC: {e}")
        return

    last_process = None
    last_window_title = None
    was_idle = False

    while True:
        idle_time = get_idle_time()
        buttons = [{"label": "Use SpyEye", "url": "https://github.com/thenameissubhan/SpyEye_Discord_RPC"}]

        if idle_time > IDLE_THRESHOLD:
            if not was_idle:
                try:
                    rpc.update(
                        state="IDLE",
                        details="No activity",
                        large_image="idle_icon",
                        large_text="IDLE",
                        start=time.time(),
                        buttons=buttons
                    )
                    print("Status: IDLE")
                    was_idle = True
                except Exception as e:
                    print(f"Error setting IDLE status: {e}")
        else:
            try:
                active_window, process_name = get_active_window_details()
                
                if was_idle or process_name != last_process or active_window != last_window_title:
                    was_idle = False
                    last_process = process_name
                    last_window_title = active_window

                    image_map = load_image_map()
                    domain_name = extract_domain_name(active_window)
                    
                    if domain_name == "YouTube":
                        state = f"Currently Watching | {active_window}"
                        if len(state) > 128:
                         state = state[:128 - len("... | **YouTube** |")]
                        image_key = "youtube_icon"
                        state = state[:128]
                    elif domain_name == "Gmail":
                        state = f"Active on | {active_window}"[:128]
                        image_key = "gmail_icon"
                    elif domain_name == "Reddit":
                        state = f"Active on | {active_window}"[:128]
                        image_key = "reddit_icon"
                    elif domain_name == "Twitch":
                        state = f"Currently Watching | {active_window}"[:128]
                        image_key = "twitch_icon"
                    elif domain_name == "Netflix":
                        state = f"Watching Now | {active_window}"[:128]
                        image_key = "netflix_icon"
                    else:
                        state = f"Active on | {active_window[:128]}"  # Limit to 128 characters
                        state = state[:128]  # Ensure state is within the limit
                        image_key = image_map.get(process_name, "default_icon")

                    rpc.update(
                        state=state,
                        details=f"Using {process_name.capitalize()}",
                        large_image=image_key,
                        large_text=process_name.capitalize(),
                        start=time.time(),
                        buttons=buttons
                    )
                    print(f"Window: {active_window} | Process: {process_name} | State: {state}")
            except Exception as e:
                print(f"Error in RPC update: {e}")

        time.sleep(0.2)  # Polling interval

def add_image_map(new_key, new_value):
    """Add a new entry to the image map."""
    image_map = load_image_map()
    if new_key in image_map:
        print(f"Error: Key '{new_key}' already exists in the image map.")
        return
    image_map[new_key] = new_value
    save_image_map(image_map)
    print(f"Image map entry '{new_key}: {new_value}' added successfully.")

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
    
    set_high_priority()
    update_discord_rpc()