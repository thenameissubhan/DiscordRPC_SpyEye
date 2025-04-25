# SECTION: Imports
import requests
import psutil
import os
import re
import time
import logging

# SECTION: Initialization
# Configure logging to spyeye.log (shared with test1.py)
logging.basicConfig(
    filename="spyeye.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# SECTION: Constants
STEAM_PROCESS_NAME = "steam.exe"
STEAM_API_URL = "https://store.steampowered.com/api/storesearch"
STEAM_GAME_PATHS = ["steamapps\\common", "SteamApps\\common"]
STEAM_STATUS_CHECK_INTERVAL = 300  # Check Steam status every 5 minutes
API_CACHE_TTL = 86400  # Cache API results for 24 hours

# SECTION: Global State
_steam_running = False
_last_steam_check = 0
_api_cache = {}  # {query: (game_name, timestamp)}
_game_folder_cache = {}  # {proc_name: game_folder} to prevent duplicate logging
_activity_cache = {}  # {proc_name: (state, details, image_key)} to prevent duplicate activity logging
_name_cache = {}  # {proc_name: game_name} to prevent duplicate name logging

# SECTION: Steam Detection Functions
def is_steam_running():
    """Check if Steam is running, caching the result for efficiency."""
    global _steam_running, _last_steam_check
    current_time = time.time()
    if current_time - _last_steam_check >= STEAM_STATUS_CHECK_INTERVAL:
        try:
            _steam_running = False
            for proc in psutil.process_iter(['name', 'exe']):
                if proc.info['name'].lower() == STEAM_PROCESS_NAME:
                    exe_path = proc.exe()
                    if 'steam' in exe_path.lower() and os.path.exists(exe_path):
                        _steam_running = True
                        logging.info(f"Steam detected: {exe_path}")
                        break
            if not _steam_running:
                logging.info("Steam is not running")
            _last_steam_check = current_time
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logging.error(f"Error checking Steam process: {e}")
            _steam_running = False
            _last_steam_check = current_time
    return _steam_running

def is_process_alive(proc_name):
    """Check if a process is still running."""
    try:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'].lower() == f"{proc_name}.exe":
                return True
        return False
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        logging.error(f"Error checking process {proc_name}: {e}")
        return False

def is_steam_game(proc_name):
    """
    Determine if the process is a Steam game.
    Returns a tuple: (is_game, game_folder_name or None).
    Logs game folder detection only once per process.
    """
    if not is_steam_running():
        logging.debug(f"No Steam running, skipping game check for: {proc_name}")
        return False, None
    
    try:
        proc = next((p for p in psutil.process_iter(['name', 'exe']) if p.info['name'].lower() == f"{proc_name}.exe"), None)
        if not proc:
            logging.debug(f"No process found for: {proc_name}.exe")
            return False, None
        
        exe_path = os.path.normpath(proc.exe())  # Preserve original case
        for steam_path in STEAM_GAME_PATHS:
            steam_path_normalized = os.path.normpath(steam_path).lower()
            if steam_path_normalized in exe_path.lower():
                path_parts = exe_path.split(os.sep.join(steam_path.split('\\')))  # Split on exact steam_path
                if len(path_parts) > 1:
                    game_folder = path_parts[1].split(os.sep)[1] if len(path_parts[1].split(os.sep)) > 1 else None
                    if game_folder:
                        if proc_name not in _game_folder_cache or _game_folder_cache[proc_name] != game_folder:
                            logging.info(f"Game folder detected: {game_folder} for process: {proc_name}")
                            _game_folder_cache[proc_name] = game_folder
                        return True, game_folder
        logging.debug(f"No Steam game path found for: {proc_name}")
        return False, None
    except (psutil.NoSuchProcess, psutil.AccessDenied, IndexError) as e:
        logging.error(f"Error accessing process {proc_name}: {e}")
        return False, None

def get_steam_game_name(exe_name, window_title, game_folder=None):
    """
    Get the proper game name, prioritizing the Steam game folder name with exact case.
    Falls back to cached API or cleaned process name.
    """
    if game_folder:
        cleaned_name = re.sub(r'[.!?]+$', '', game_folder).strip()
        if cleaned_name:
            if exe_name not in _name_cache or _name_cache[exe_name] != cleaned_name:
                logging.info(f"Using folder name: {cleaned_name}")
                _name_cache[exe_name] = cleaned_name
            return cleaned_name
    
    search_query = exe_name.replace('_', ' ').replace('-', ' ').split('.')[0].strip()
    if not search_query or len(search_query) < 3:
        search_query = window_title.split('-')[0].strip()

    current_time = time.time()
    if search_query in _api_cache:
        game_name, timestamp = _api_cache[search_query]
        if current_time - timestamp < API_CACHE_TTL:
            logging.debug(f"Using cached API name: {game_name} for query: {search_query}")
            return game_name
        else:
            del _api_cache[search_query]

    try:
        response = requests.get(
            STEAM_API_URL,
            params={"term": search_query, "l": "english", "cc": "us"},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        if data.get("total", 0) > 0:
            game_name = data["items"][0]["name"]
            _api_cache[search_query] = (game_name, current_time)
            logging.info(f"Steam API returned: {game_name} for query: {search_query}")
            return game_name
        else:
            cleaned_name = search_query.title()
            _api_cache[search_query] = (cleaned_name, current_time)
            logging.info(f"Fallback to cleaned name: {cleaned_name}")
            return cleaned_name
    except Exception as e:
        logging.error(f"Steam API error for query {search_query}: {e}")
        cleaned_name = search_query.title()
        _api_cache[search_query] = (cleaned_name, current_time)
        logging.info(f"Fallback to cleaned name: {cleaned_name}")
        return cleaned_name

def get_steam_game_activity(proc_name, active_title, image_map):
    """
    Get the state, details, and image key for a Steam game.
    Returns (state, details, image_key).
    Logs activity only once per unique activity.
    """
    is_game, game_folder = is_steam_game(proc_name)
    if not is_game:
        logging.warning(f"Non-Steam process in get_steam_game_activity: {proc_name}")
    game_name = get_steam_game_name(proc_name, active_title, game_folder)
    state = f"Playing {game_name}"
    details = "Via Steam"
    image_key = image_map.get(proc_name, "default_game_icon")
    
    current_activity = (state, details, image_key)
    if proc_name not in _activity_cache or _activity_cache[proc_name] != current_activity:
        logging.info(f"Steam activity: state={state}, details={details}, image_key={image_key}")
        _activity_cache[proc_name] = current_activity
    
    return state, details, image_key

# SECTION: Entry Point (for testing)
if __name__ == "__main__":
    # Test the functions
    proc_name = "GolfIt"  # Replace with a test process name
    is_game, folder = is_steam_game(proc_name)
    print(f"Is {proc_name} a Steam game? {is_game}, Folder: {folder}")
    if is_game:
        name = get_steam_game_name(proc_name, "Golf It - Main Menu", folder)
        activity = get_steam_game_activity(proc_name, "Golf It - Main Menu", {})
        print(f"Game Name: {name}")
        print(f"Activity: {activity}")