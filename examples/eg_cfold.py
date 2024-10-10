import os
import shutil
from typing import List

def copy_subfolders(source_dir: str, target_dir: str, sub_sub_folder_names: List[str], num_sub_folders_to_copy: int):
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"{source_dir} does not exist.")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    sub_folders = [f.path for f in os.scandir(source_dir) if f.is_dir()]
    
    if len(sub_folders) == 0:
        raise ValueError("No sub-folders available to copy.")
    
    copied_count = 0
    for sub_folder in sub_folders:
        if copied_count >= num_sub_folders_to_copy:
            break
        
        target_sub_folder = os.path.basename(sub_folder)

        # ## copy all files the sub folder to the target folder
        for file in os.listdir(sub_folder):
            # Check if the file is a regular file
            if os.path.isfile(os.path.join(source_dir, file)):
                # Copy the file to the destination directory
                shutil.copy(os.path.join(source_dir, file), target_sub_folder)
                print(f"Copied {file} to {target_sub_folder}")
                        
        copied = False
        for sub_sub_folder_name in sub_sub_folder_names:
            source_path = os.path.join(sub_folder, sub_sub_folder_name)
            if not os.path.exists(source_path):
                print(f"Skipping {source_path} as it does not exist.")
                continue
                
            target_path = os.path.join(target_dir, target_sub_folder, sub_sub_folder_name)
            if os.path.exists(target_path):
                print(f"Skipping {target_path} as it already exists.")
            else:
                shutil.copytree(source_path, target_path)
                print(f"Copied {source_path} to {target_path}")
                copied = True

        if copied:
            copied_count += 1 # Increment the copied_count if at least one sub_sub_folder was copied
        

if __name__ == "__main__":
    # replace these variables with actual input
    source_dir = r'C:\Users\raman\OneDrive\Desktop\Testing\Source'
    target_dir = r'C:\Users\raman\OneDrive\Desktop\Testing\Target'
    sub_sub_folder_names = ['docs', 'results']
    num_sub_folders_to_copy = 1  # replace with the number of sub-folders you want to copy

    copy_subfolders(source_dir, target_dir, sub_sub_folder_names, num_sub_folders_to_copy)