from pypresence import Presence
from domain_extractor import extract_domain_name
from activity_state import get_activity_state_and_image
from image_map import load_image_map
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
CLIENT_ID_FILE = "client_id.json"
IMAGE_MAP_FILE = "image_map.json"
DEFAULT_CLIENT_ID = "1314279361582596146"
IDLE_THRESHOLD = 10800  # 3 hours idle timeout


def set_high_priority():
    """Set the script process to high priority."""
    p = psutil.Process(os.getpid())
    p.nice(psutil.HIGH_PRIORITY_CLASS)


def load_client_id():
    """Load the Discord client ID from a JSON file or return the default."""
    if os.path.exists(CLIENT_ID_FILE):
        with open(CLIENT_ID_FILE, "r") as f:
            data = json.load(f)
            return data.get("client_id", DEFAULT_CLIENT_ID)
    return DEFAULT_CLIENT_ID


def save_client_id(client_id):
    """Save a new client ID to the JSON file."""
    with open(CLIENT_ID_FILE, "w") as f:
        json.dump({"client_id": client_id}, f)


IMAGE_MAP_FILE = "image_map.json"


def load_image_map():
    """Load the image map from a JSON file or return an empty dict."""
    if os.path.exists(IMAGE_MAP_FILE):
        with open(IMAGE_MAP_FILE, "r") as f:
            return json.load(f)
    return {}  # return empty if file doesn't exist


def save_image_map(image_map):
    """Save the updated image map to the JSON file."""
    with open(IMAGE_MAP_FILE, "w") as f:
        json.dump(image_map, f, indent=4)


def get_client_id():
    """Retrieve the current client ID."""
    return load_client_id()


def get_idle_time():
    """Calculate the time since last user input in seconds."""
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0


def get_active_window_details():
    """Get the title and process name of the active window."""
    try:
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            return "Unknown Window", "unknown"
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        proc = psutil.Process(pid)
        pname = proc.name().lower().replace(".exe", "")
        title = win32gui.GetWindowText(hwnd) or "Untitled"
        return title, pname
    except Exception:
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

    last_sent_process = None
    last_sent_title = None
    last_valid_process = None
    last_valid_title = None
    was_idle = False

    while True:
        idle = get_idle_time()
        buttons = [
            {
                "label": "Use SpyEye",
                "url": "https://github.com/thenameissubhan/SpyEye_Discord_RPC",
            }
        ]

        # IDLE handling
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
                    was_idle = True
                except Exception as e:
                    print(f"Error setting IDLE status: {e}")
        else:
            # Get current window
            active_title, proc_name = get_active_window_details()

            # If this is a “desktop” or unknown window, fall back to the last valid app
            if proc_name == "unknown" or active_title == "Unknown Window":
                if last_valid_process and last_valid_title:
                    proc_name = last_valid_process
                    active_title = last_valid_title
            else:
                # Otherwise update our “last valid” tracker
                last_valid_process = proc_name
                last_valid_title = active_title

            # Only send a new update if something actually changed (or we were idle)
            if (
                was_idle
                or proc_name != last_sent_process
                or active_title != last_sent_title
            ):
                was_idle = False
                last_sent_process = proc_name
                last_sent_title = active_title

                state, details, image_key = get_activity_state_and_image(
                    proc_name, active_title
                )

                # Send the update
                try:
                    rpc.update(
                        state=state,
                        details=details,
                        large_image=image_key,
                        large_text=proc_name.capitalize(),
                        small_image="spyeye",
                        small_text="SpyEye Active",
                        start=time.time(),
                        buttons=buttons,
                    )
                    print(f"Updated → {proc_name}: {active_title}")
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
