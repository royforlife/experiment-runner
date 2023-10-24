import os
import random
import shutil

PARENT_DIR = os.path.join(os.getcwd(), "..")
TARGET_SIZE = 5 * 1024 * 1024 * 1024  # 5GB in bytes using the 1GB = 1024MB convention
NEW_FOLDER = os.path.join(PARENT_DIR, "select")

def get_files_from_directory(directory):
    with os.scandir(directory) as entries:
        return [entry.path for entry in entries if entry.is_file()]

def select_files(files, target_size):
    random.shuffle(files)
    
    selected_files = []
    total_size = 0
    
    for file in files:
        file_size = os.path.getsize(file)
        if total_size + file_size > target_size:
            continue
        
        selected_files.append(file)
        total_size += file_size
        
        if total_size >= target_size:
            break
            
    return selected_files

def move_files_to_new_folder(files, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    for file in files:
        shutil.move(file, destination_folder)

files = get_files_from_directory(PARENT_DIR)
selected_files = select_files(files, TARGET_SIZE)

print(f"Selected {len(selected_files)} files totaling {sum(os.path.getsize(f) for f in selected_files) / (1024 * 1024 * 1024):.2f} GB:")
move_files_to_new_folder(selected_files, NEW_FOLDER)
print(f"Moved selected files to {NEW_FOLDER}")
