import os
import shutil
import json
from pathlib import Path

def load_settings():
    """Load user settings from the JSON config file."""
    with open('config/settings.json', 'r') as f:
        return json.load(f)

def sort_files(target_path):
    """The core logic to sort files in a given directory."""
    path = Path(target_path)
    
    if not path.exists():
        print(f"Error: {path} does not exist.")
        return

    # Load categories from our new JSON file
    settings = load_settings()
    extensions_map = settings["categories"]

    files = os.listdir(path)

    for file_name in files:
        file_path = path / file_name # Using pathlib for cleaner path joining
        
        if file_path.is_dir():
            continue

        ext = file_path.suffix.lower()
        moved = False

        for folder_name, extensions in extensions_map.items():
            if ext in extensions:
                dest_folder = path / folder_name
                dest_folder.mkdir(exist_ok=True)
                shutil.move(str(file_path), str(dest_folder / file_name))
                print(f"Moved: {file_name} → {folder_name}")
                moved = True
                break

        if not moved:
            others_folder = path / "Others"
            others_folder.mkdir(exist_ok=True)
            shutil.move(str(file_path), str(others_folder / file_name))
            print(f"Moved: {file_name} → Others")

if __name__ == "__main__":
    # For testing, we can still run it manually
    user_input = input("Enter folder path to sort: ").strip()
    sort_files(user_input)

