import json
import os

IMAGE_MAP_FILE = "image_map.json"

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
    "mspaint": "mspaint_icon",
    "windowsterminal": "windowsterminal_icon",
    "excel": "excel_icon",
    "mmc": "mmc_icon",
    "unrealeditor": "unrealeditor_icon",
    "winword": "winword_icon",
    "powerpnt": "powerpnt_icon",
    "unknown": "default_icon"
}


def load_image_map():
    if os.path.exists(IMAGE_MAP_FILE):
        with open(IMAGE_MAP_FILE, "r") as f:
            return json.load(f)
    else:
        save_image_map(DEFAULT_IMAGE_MAP)
        return DEFAULT_IMAGE_MAP.copy()


def save_image_map(image_map):
    # Ensure "unknown" is always at the end
    image_map = {
        k: v for k, v in image_map.items() if k != "unknown"
    }
    image_map["unknown"] = "default_icon"
    with open(IMAGE_MAP_FILE, "w") as f:
        json.dump(image_map, f, indent=4)


def add_image_map(new_key, new_value):
    image_map = load_image_map()
    if new_key in image_map:
        print(f"Error: Key '{new_key}' already exists.")
        return

    # Insert new key-value pair before "unknown"
    image_map_items = list(image_map.items())
    updated_items = []

    for k, v in image_map_items:
        if k == "unknown":
            updated_items.append((new_key, new_value))
        updated_items.append((k, v))

    updated_map = dict(updated_items)
    save_image_map(updated_map)
    print(f"Added '{new_key}': '{new_value}' to image map.")
