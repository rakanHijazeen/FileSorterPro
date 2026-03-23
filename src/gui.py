import os
import sys

# MANUALLY POINT TO TCL/TK (The Permanent Fix)
os.environ['TCL_LIBRARY'] = r'C:/Users/user/AppData/Local/Programs/Python/Python313/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = r'C:/Users/user/AppData/Local/Programs/Python/Python313/tcl/tk8.6'

import customtkinter as ctk
import json
import threading
import time
from pathlib import Path
from tkinter import filedialog
from watchdog.observers import Observer
from monitor import SortHandler
from sorter import sort_files

# UI Theme Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SortFlowGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup.
        self.title("SortFlow Pro")
        self.geometry("700x500")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.observer = None  # To hold the background monitor

        # Sidebar.
        self.sidebar = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.logo_label = ctk.CTkLabel(self.sidebar, text="SortFlow", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Path Selection.
        self.path_label = ctk.CTkLabel(self, text="Target Directory:", anchor="w")
        self.path_label.grid(row=0, column=1, padx=20, pady=(20, 0), sticky="w")

        self.path_entry = ctk.CTkEntry(self, placeholder_text="Select a folder to watch...")
        self.path_entry.grid(row=1, column=1, padx=(20, 10), pady=(0, 20), sticky="ew")

        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.browse_folder, width=100)
        self.browse_button.grid(row=1, column=2, padx=(0, 20), pady=(0, 20))

        # Controls (Manual Sort & Automation Switch).
        self.sort_button = ctk.CTkButton(self, text="Sort Now", fg_color="green", hover_color="#228B22", command=self.manual_sort)
        self.sort_button.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        self.auto_switch_var = ctk.StringVar(value="off")
        self.auto_switch = ctk.CTkSwitch(self, text="Real-time Automation", 
                                         command=self.toggle_automation,
                                         variable=self.auto_switch_var, 
                                         onvalue="on", offvalue="off")
        self.auto_switch.grid(row=2, column=1, padx=(180, 20), pady=10, sticky="w")

        # Log / Console Area.
        self.log_textbox = ctk.CTkTextbox(self, width=250, height=200)
        self.log_textbox.grid(row=3, column=1, columnspan=2, padx=20, pady=(10, 20), sticky="nsew")
        self.log_textbox.insert("0.0", "System Ready...\n")

        config_path = Path(__file__).parent.parent / "config" / "settings.json"
        if config_path.exists():
            with open(config_path, "r") as f:
                data = json.load(f)
                # This automatically puts the saved path into the box on startup!
                self.path_entry.insert(0, data.get("watch_directory", ""))
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            # 1. Update the UI
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)
            
            # 2. Update the config/settings.json file
            try:
                config_path = Path(__file__).parent.parent / "config" / "settings.json"
                with open(config_path, "r") as f:
                    data = json.load(f)
                
                data["watch_directory"] = folder  # Change the old path to the new one
                
                with open(config_path, "w") as f:
                    json.dump(data, f, indent=4)
                    
                self.log_textbox.insert("end", f"⚙️ Configuration updated to: {folder}\n")
            except Exception as e:
                self.log_textbox.insert("end", f"⚠️ Failed to save settings: {e}\n")
    def manual_sort(self):
        target = self.path_entry.get()
        if target:
            self.log_textbox.insert("end", f"Starting manual sort on: {target}\n")
            sort_files(target)
            self.log_textbox.insert("end", "✅ Manual Sort Complete.\n")
            self.log_textbox.see("end") # Auto-scroll to bottom

    def toggle_automation(self):
        target = self.path_entry.get()
        if not target:
            self.log_textbox.insert("end", "⚠️ Error: Select a path first!\n")
            self.auto_switch.deselect()
            return

        if self.auto_switch_var.get() == "on":
            self.log_textbox.insert("end", f"🚀 Automation Started: Monitoring {Path(target).name}...\n")
            # Start monitor in a background thread
            self.monitor_thread = threading.Thread(target=self.run_monitor, args=(target,), daemon=True)
            self.monitor_thread.start()
        else:
            if self.observer:
                self.observer.stop()
                self.log_textbox.insert("end", "🛑 Automation Stopped.\n")

    def run_monitor(self, path):
        """Logic for the background thread."""
        event_handler = SortHandler(path)
        self.observer = Observer()
        self.observer.schedule(event_handler, path, recursive=False)
        self.observer.start()
        try:
            while self.observer.is_alive():
                time.sleep(1)
        except Exception as e:
            self.observer.stop()
    
if __name__ == "__main__":
    app = SortFlowGUI()
    app.mainloop()