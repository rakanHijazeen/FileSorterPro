# SortFlow Pro: Real-Time File Automation

A professional-grade desktop application built with Python that monitors directories and automatically categorizes files into structured folders based on file types.

Designed to eliminate "Download Folder Chaos" for power users and developers.

---

## Key Features

- **Real-Time Monitoring:** Uses the `watchdog` library to detect new files the millisecond they land in your folder.
- **Multi-Threaded GUI:** Built with `CustomTkinter`, utilizing Python's `threading` module to ensure the interface remains responsive during background sorting.
- **Smart Conflict Resolution:** Automatically renames files with timestamps if a duplicate exists, preventing data loss.
- **Bulletproof Error Handling:** Specifically handles Windows `PermissionError` (locked files) without crashing the service.
- **Modern UI:** Dark-mode optimized interface with live activity logging.

---

## Tech Stack

- **Language:** Python 3.13
- **GUI Framework:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- **File System Events:** [Watchdog](https://github.com/gorakhargosh/watchdog)
- **Architecture:** Modular (Separation of Concerns between Logic, Monitor, and UI)

---

## Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/rakanHijazeen/FileSorterPro.git](https://github.com/rakanHijazeen/FileSorterPro.git)
   cd FileSorterPro

   ```

2. Create and Activate Virtual Environment:

bash:
python -m venv .venv
source .venv/Scripts/activate # On Windows

3. Install Dependencies:

bash:
pip install -r requirements.txt

(Note: If requirements.txt isn't present, run pip install customtkinter watchdog)

4. Launch the Application:

bash:
python src/main.py

-- How It Works
Select Path: Use the "Browse" button to pick a messy folder (e.g., Downloads).

Manual Sort: Click "Sort Now" to organize existing files instantly.

Automate: Toggle "Real-time Automation" to let SortFlow run in the background. It will watch for new files and move them into categorized subfolders (Documents, Images, Media, etc.) automatically.

-- Technical Highlights
The Threading Challenge: Implemented threading.Thread(daemon=True) to decouple the File Observer from the Main Loop, preventing GUI freezing.

Windows Path Resilience: Integrated self-healing Tcl/Tk path environment variables to ensure cross-device compatibility on Windows systems.
