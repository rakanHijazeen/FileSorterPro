import os 
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sorter import sort_files # Importing your logic from the other file

class SortHandler(FileSystemEventHandler):
    def __init__(self, watch_path):
        self.watch_path = watch_path

    def on_modified(self, event):
        # We trigger the sorter whenever the folder changes
        if not event.is_directory:
            print(f"Event detected: {event.src_path}. Sorting...")
            sort_files(self.watch_path)

def start_monitoring():
    # Load the path from your new config/settings.json
    with open('config/settings.json', 'r') as f:
        settings = json.load(f)
    
    path_to_watch = settings["watch_directory"]
    
    if not os.path.exists(path_to_watch):
        print(f"Error: The directory '{path_to_watch}' was not found.")
        print("Please check your config/settings.json and ensure the folder exists.")
        return
    
    event_handler = SortHandler(path_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    
    print(f"Monitoring started on: {path_to_watch}")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_monitoring()