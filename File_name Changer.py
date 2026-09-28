import os
from pathlib import Path

# Directory containing this script
script_path = Path(__file__).resolve()
root_path = script_path.parent

counter = 1

# Only files directly in this folder (not subfolders), skipping this script itself
filenames = sorted(
    f for f in os.listdir(root_path)
    if (root_path / f).is_file() and f != script_path.name
)

for filename in filenames:
    old_full_path = root_path / filename
    extension = old_full_path.suffix
    new_name = f"{counter}{extension}"
    new_full_path = root_path / new_name

    try:
        print(f"Renaming: {filename} -> {new_name}")
        os.rename(old_full_path, new_full_path)
        counter += 1
    except Exception as e:
        print(f"Error renaming {filename}: {e}")

print(f"Done! Renamed {counter - 1} total files.")
