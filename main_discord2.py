# SECTION: Imports
from pypresence import Presence
from domain_extractor import extract_domain_name
from activity_state import get_activity_state_and_image
from image_map import load_image_map
from steam_game_detector import is_steam_game, get_steam_game_activity, is_process_alive
import win32gui
import win32process
import psutil
import time
import json
import os
import sys
import win32api
import GPUtil
import wmi
import logging

# Wait for 30 seconds before starting the rest of the script
time.sleep(30)

# SECTION: Initialization
# Configure logging
logging.basicConfig(
    filename="spyeye.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# SECTION: Constants
CLIENT_ID_FILE = "client_id.json"
IMAGE_MAP_FILE = "image_map.json"
DEFAULT_CLIENT_ID = "1314279361582596146"
IDLE_THRESHOLD = 10800  # 3 hours
CONSOLE_CLEAR_INTERVAL = 1800  # 30 minutes
POLLING_INTERVAL = 0.5  # Faster polling for window detection
RECONNECT_ATTEMPTS = 5
RECONNECT_DELAY = 10  # Seconds

# SECTION: Global State
_activity_cache = {}  # {proc_name: (state, details, image_key, small_image, small_text, buttons)} for RPC updates
_rpc_log_cache = {}  # {proc_name: (state, details, image_key)} for logging
_last_game_process = None  # Track last Steam game process

# SECTION: Utility Functions
def set_high_priority():
    """Set the script process to high priority."""
    try:
        p = psutil.Process(os.getpid())
        p.nice(psutil.HIGH_PRIORITY_CLASS)
        logging.info("Set high priority for process")
    except Exception as e:
        logging.error(f"Error setting high priority: {e}")

def load_client_id():
    """Load the Discord client ID from a JSON file or return the default."""
    try:
        if os.path.exists(CLIENT_ID_FILE):
            with open(CLIENT_ID_FILE, "r") as f:
                data = json.load(f)
                return data.get("client_id", DEFAULT_CLIENT_ID)
        save_client_id(DEFAULT_CLIENT_ID)
        return DEFAULT_CLIENT_ID
    except Exception as e:
        logging.error(f"Error loading client ID: {e}")
        return DEFAULT_CLIENT_ID

def save_client_id(client_id):
    """Save a new client ID to the JSON file."""
    try:
        with open(CLIENT_ID_FILE, "w") as f:
            json.dump({"client_id": client_id}, f)
        logging.info(f"Saved client ID: {client_id}")
    except Exception as e:
        logging.error(f"Error saving client ID: {e}")

def load_image_map_cached():
    """Load and cache the image map from a JSON file."""
    if not hasattr(load_image_map_cached, "cache"):
        try:
            load_image_map_cached.cache = load_image_map() if os.path.exists(IMAGE_MAP_FILE) else {}
            logging.info("Loaded and cached image map")
        except Exception as e:
            logging.error(f"Error loading image map: {e}")
            load_image_map_cached.cache = {}
    return load_image_map_cached.cache

def save_image_map(image_map):
    """Save the updated image map to the JSON file and update cache."""
    try:
        with open(IMAGE_MAP_FILE, "w") as f:
            json.dump(image_map, f, indent=4)
        load_image_map_cached.cache = image_map
        logging.info("Saved and updated image map cache")
    except Exception as e:
        logging.error(f"Error saving image map: {e}")

def get_client_id():
    """Retrieve the current client ID."""
    return load_client_id()

def get_idle_time():
    """Calculate the time since last user input in seconds."""
    try:
        return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0
    except Exception as e:
        logging.error(f"Error getting idle time: {e}")
        return 0.0

def clear_console():
    """Clear the console output (Windows-specific)."""
    try:
        os.system("cls")
        logging.info("Cleared console")
    except Exception as e:
        logging.error(f"Error clearing console: {e}")

def detect_gpu_vendor():
    """Detect the GPU vendor (NVIDIA, AMD, Intel) at startup."""
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            logging.info("Detected NVIDIA GPU")
            return "NVIDIA"
    except Exception:
        pass

    try:
        import pyadl
        devices = pyadl.ADLManager.getInstance().getDevices()
        if devices:
            logging.info("Detected AMD GPU")
            return "AMD"
    except Exception:
        pass

    try:
        w = wmi.WMI(namespace="root\\CIMV2")
        for gpu in w.Win32_PerfFormattedData_Counter_GPUProcessMemory():
            if "Intel" in gpu.Name:
                logging.info("Detected Intel GPU")
                return "Intel"
    except Exception:
        pass

    logging.warning("No supported GPU detected")
    return None

def get_gpu_metrics(vendor):
    """Get GPU usage and temperature based on detected vendor."""
    if not vendor:
        return 0.0, 0.0

    if vendor == "NVIDIA":
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                return gpus[0].load * 100, gpus[0].temperature
        except Exception as e:
            logging.error(f"NVIDIA GPU metrics error: {e}")
            return 0.0, 0.0

    if vendor == "AMD":
        try:
            import pyadl
            devices = pyadl.ADLManager.getInstance().getDevices()
            if devices:
                return devices[0].getCurrentUsage(), devices[0].getCurrentTemperature()
        except Exception as e:
            logging.error(f"AMD GPU metrics error: {e}")
            return 0.0, 0.0

    if vendor == "Intel":
        try:
            w = wmi.WMI(namespace="root\\CIMV2")
            for gpu in w.Win32_PerfFormattedData_Counter_GPUProcessMemory():
                if "Intel" in gpu.Name:
                    usage = float(gpu.PercentProcessorTime) / 100.0
                    return usage, 0.0  # Temperature not available
        except Exception as e:
            logging.error(f"Intel GPU metrics error: {e}")
            return 0.0, 0.0

    return 0.0, 0.0

def get_active_window_details():
    """Get the title and process name of the active window."""
    try:
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd or not win32gui.IsWindowVisible(hwnd):
            logging.debug("No visible foreground window detected")
            return "Desktop", "explorer"
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        proc = psutil.Process(pid)
        pname = proc.name().lower().replace(".exe", "")
        title = win32gui.GetWindowText(hwnd) or "Untitled"
        return title, pname
    except (psutil.NoSuchProcess, psutil.AccessDenied, Exception) as e:
        logging.error(f"Error getting active window details: {e}")
        return "Desktop", "explorer"

# SECTION: Main Logic
def connect_rpc(client_id):
    """Connect to Discord RPC with retry logic."""
    for attempt in range(RECONNECT_ATTEMPTS):
        try:
            rpc = Presence(client_id)
            rpc.connect()
            logging.info("RPC connected successfully")
            return rpc
        except Exception as e:
            logging.error(f"RPC connection attempt {attempt + 1} failed: {e}")
            if attempt < RECONNECT_ATTEMPTS - 1:
                time.sleep(RECONNECT_DELAY)
    logging.critical("Failed to connect to RPC after all attempts")
    return None

def update_activity(rpc, state, details, image_key, small_image, small_text, buttons, start_time):
    """Update Discord Rich Presence with the given activity."""
    global _activity_cache, _rpc_log_cache
    try:
        proc_name = get_active_window_details()[1]
        # Cache for RPC updates (includes small_text and buttons for real-time GPU metrics)
        activity_key = (state, details, image_key, small_image, small_text, tuple(buttons))
        # Cache for logging (excludes small_text and buttons to avoid logging on GPU changes)
        log_key = (state, details, image_key)

        # Update RPC if activity changes
        if proc_name not in _activity_cache or _activity_cache[proc_name] != activity_key:
            rpc.update(
                state=state,
                details=details,
                large_image=image_key,
                large_text=state,
                small_image=small_image,
                small_text=small_text,
                start=start_time,
                buttons=buttons,
            )
            _activity_cache[proc_name] = activity_key

        # Log only if core activity changes
        if proc_name not in _rpc_log_cache or _rpc_log_cache[proc_name] != log_key:
            logging.info(f"Updated RPC: {state} - {details}")
            _rpc_log_cache[proc_name] = log_key
    except Exception as e:
        logging.error(f"Error updating RPC: {e}")

def update_discord_rpc():
    """Main loop to update Discord Rich Presence."""
    global _last_game_process
    client_id = get_client_id()
    rpc = connect_rpc(client_id)
    if not rpc:
        print("Failed to connect to Discord RPC. Exiting.")
        logging.critical("Exiting due to RPC connection failure")
        return

    gpu_vendor = detect_gpu_vendor()
    was_idle = False
    last_clear_time = time.time()
    last_valid_process = None
    last_valid_title = None
    last_sent_process = None
    last_sent_title = None
    last_gpu_usage = None
    last_gpu_temp = None

    while True:
        try:
            current_time = time.time()
            if current_time - last_clear_time >= CONSOLE_CLEAR_INTERVAL:
                clear_console()
                last_clear_time = current_time

            idle = get_idle_time()
            buttons = [{"label": "Use SpyEye", "url": "https://github.com/thenameissubhan/SpyEye_Discord_RPC"}]

            if idle > IDLE_THRESHOLD:
                if not was_idle:
                    try:
                        rpc.update(
                            state="IDLE",
                            details="No activity",
                            large_image="idle_icon",
                            large_text="IDLE",
                            small_image="spyeye",
                            small_text="SpyEye Active",
                            start=time.time(),
                            buttons=buttons,
                        )
                        print("Status: IDLE")
                        logging.info("Updated RPC: IDLE - No activity")
                        was_idle = True
                    except Exception as e:
                        logging.error(f"Error setting IDLE status: {e}")
            else:
                # Get current window
                active_title, proc_name = get_active_window_details()

                # If this is a “desktop” or unknown window, fall back to the last valid app
                if proc_name == "unknown" or active_title == "Desktop":
                    if last_valid_process and last_valid_title:
                        proc_name = last_valid_process
                        active_title = last_valid_title
                else:
                    # Otherwise update our “last valid” tracker
                    last_valid_process = proc_name
                    last_valid_title = active_title

                # Check if last Steam game process terminated
                if _last_game_process and not is_process_alive(_last_game_process):
                    if _last_game_process in _activity_cache:
                        del _activity_cache[_last_game_process]
                    if _last_game_process in _rpc_log_cache:
                        del _rpc_log_cache[_last_game_process]
                    logging.info(f"Steam game process {_last_game_process} terminated, forcing update")
                    _last_game_process = None

                # Force update if window changes
                if (
                    was_idle
                    or proc_name != last_sent_process
                    or active_title != last_sent_title
                ):
                    was_idle = False
                    last_sent_process = proc_name
                    last_sent_title = active_title

                    # Clear caches for this proc_name to force update
                    if proc_name in _activity_cache:
                        del _activity_cache[proc_name]
                    if proc_name in _rpc_log_cache:
                        del _rpc_log_cache[proc_name]

                    print(f"Updated → {proc_name}: {active_title}")
                    logging.info(f"Active window: {proc_name} - {active_title}")

                    is_game, game_folder = is_steam_game(proc_name)
                    if proc_name == "steam":
                        state = "Using Steam"
                        details = "In Library" if "Library" in active_title else "Browsing Steam"
                        image_key = "steam_icon"
                        small_image = "spyeye"
                        small_text = "SpyEye Active"
                        start_time = time.time()
                    elif is_game and proc_name != "unknown":
                        _last_game_process = proc_name
                        image_map = load_image_map_cached()
                        state, details, image_key = get_steam_game_activity(proc_name, active_title, image_map)
                        gpu_usage, gpu_temp = get_gpu_metrics(gpu_vendor)
                        if (
                            abs(gpu_usage - (last_gpu_usage or 0)) > 1 or
                            abs(gpu_temp - (last_gpu_temp or 0)) > 1
                        ):
                            last_gpu_usage = gpu_usage
                            last_gpu_temp = gpu_temp
                        buttons = [
                            {"label": f"GPU Usage: {gpu_usage:.1f}%", "url": "https://github.com/thenameissubhan/SpyEye_Discord_RPC"},
                            {"label": f"GPU Temp: {gpu_temp:.1f}°C", "url": "https://github.com/thenameissubhan/SpyEye_Discord_RPC"}
                        ]
                        small_image = "steam_icon"
                        small_text = f"GPU: {gpu_usage:.1f}%"
                        start_time = time.time()
                    else:
                        state, details, image_key = get_activity_state_and_image(proc_name, active_title)
                        small_image = "spyeye"
                        small_text = "SpyEye Active"
                        start_time = time.time()

                    update_activity(
                        rpc=rpc,
                        state=state,
                        details=details,
                        image_key=image_key,
                        small_image=small_image,
                        small_text=small_text,
                        buttons=buttons,
                        start_time=start_time
                    )

            time.sleep(POLLING_INTERVAL)
        except Exception as e:
            logging.error(f"Main loop error: {e}")
            time.sleep(POLLING_INTERVAL)

# SECTION: Image Map Management
def add_image_map(new_key, new_value):
    """Add a new entry to the image map."""
    try:
        image_map = load_image_map_cached()
        if new_key in image_map:
            print(f"Error: Key '{new_key}' already exists in the image map.")
            logging.error(f"Attempted to add duplicate image map key: {new_key}")
            return
        image_map[new_key] = new_value
        save_image_map(image_map)
        print(f"Image map entry '{new_key}: {new_value}' added successfully.")
        logging.info(f"Added image map entry: {new_key} = {new_value}")
    except Exception as e:
        logging.error(f"Error adding image map entry: {e}")

# SECTION: Entry Point
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--update-client-id":
            if len(sys.argv) > 2:
                save_client_id(sys.argv[2])
                print("Client ID updated successfully.")
            else:
                print("Error: No client ID provided.")
            sys.exit(0)
        elif sys.argv[1] == "--add-image-map":
            if len(sys.argv) > 3:
                add_image_map(sys.argv[2], sys.argv[3])
            else:
                print("Error: Usage: --add-image-map <key> <value>")
            sys.exit(0)

    set_high_priority()
    update_discord_rpc()