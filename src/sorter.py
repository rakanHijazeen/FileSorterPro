import os,shutil
from pathlib import Path
path = Path(input("Enter the folder path: ").strip())

file=os.listdir(path)

if not path.exists():
    print("Error: The specified path does not exist.")
    exit()

EXTENSIONS = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".csv", ".xls", ".xlsx", ".log"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programs": [".exe", ".msi", ".bat", ".sh", ".py", ".jar"]
}

for FILE in file:
    file_path = os.path.join(path, FILE)
    
   
    if os.path.isdir(file_path):#ignore and skip folders
        continue


    name, ext = os.path.splitext(FILE)#split file name into "name" & ".extension"
    ext = ext.lower()

    #matching 
    moved = False
    for folder_name, extensions in EXTENSIONS.items():
        if ext in extensions:
            folder_path = os.path.join(path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            shutil.move(file_path, os.path.join(folder_path, FILE))
            print(f"Moved: {FILE} → {folder_name}")
            moved = True
            break

    # If not found, move to "Others"
    if not moved:
        misc_folder = os.path.join(path, "Others")
        os.makedirs(misc_folder, exist_ok=True)
        shutil.move(file_path, os.path.join(misc_folder, FILE))
        print(f"Moved: {FILE} → Others")

