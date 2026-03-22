import os
import shutil
import json
import time
from pathlib import Path

def load_settings():
    """Load user settings from the JSON config file."""
    # We use a relative path from the root of FileSorterPro
    config_path = Path('config/settings.json')
    if not config_path.exists():
        return None
    with open(config_path, 'r') as f:
        return json.load(f)

def sort_files(target_path):
    """The core logic to sort files in a given directory with safety checks."""
    path = Path(target_path)
    
    if not path.exists():
        print(f"Error: {path} does not exist.")
        return

    settings = load_settings()
    if not settings:
        print("Error: Configuration file not found.")
        return
        
    extensions_map = settings["categories"]

    #the modern pathlib way to loop through files
    for file_path in path.iterdir():
        # Skip directories and the config folder itself if it's inside
        if file_path.is_dir():
            continue

        file_name = file_path.name
        ext = file_path.suffix.lower()
        moved = False

        # Determine destination folder
        chosen_folder = "Others"
        for folder_name, extensions in extensions_map.items():
            if ext in extensions:
                chosen_folder = folder_name
                break

        dest_folder = path / chosen_folder
        dest_folder.mkdir(exist_ok=True)
        
        # --- FEATURE: Conflict Resolution ---
        # If 'file.txt' exists, rename to 'file_1711123456.txt'
        final_dest = dest_folder / file_name
        if final_dest.exists():
            timestamp = int(time.time())
            final_dest = dest_folder / f"{file_path.stem}_{timestamp}{ext}"

        # --- FEATURE: Error Handling ---
        try:
            # We use str() because shutil sometimes prefers strings over Path objects on older Python
            shutil.move(str(file_path), str(final_dest))
            print(f"✅ Moved: {file_name} → {chosen_folder}")
        except PermissionError:
            print(f"⚠️ Access Denied: '{file_name}' is likely open in another program.")
        except Exception as e:
            print(f"❌ Unexpected Error moving {file_name}: {e}")

if __name__ == "__main__":
    # Load path from settings as default, or take manual input
    settings = load_settings()
    default_path = settings.get("watch_directory", "") if settings else ""
    
    print(f"Default watch path: {default_path}")
    user_input = input("Press Enter to sort default or type a new path: ").strip()
    
    target = user_input if user_input else default_path
    if target:
        sort_files(target)
    else:
        print("No path provided.")