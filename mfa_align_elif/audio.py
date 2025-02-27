import pandas as pd
import os
import shutil

# Define paths
csv_file = "cleaned_mfa_dataset.csv"  # Your cleaned dataset
audio_source_folder = "corpus"  # Folder where all audio files are stored
destination_folder = "removed_audios"  # Folder where cleaned audios will be moved

# Ensure destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Load cleaned dataset
df = pd.read_csv(csv_file)

# Move files to corpus/
moved_files = 0
for filename in df["path"]:  # "path" column has audio filenames
    source_path = os.path.join(audio_source_folder, filename)
    destination_path = os.path.join(destination_folder, filename)

    if os.path.exists(source_path):  # Check if file exists
        shutil.copy(source_path, destination_path)  # Copy file
        moved_files += 1
    else:
        print(f"❌ File not found: {source_path}")

print(f"✅ {moved_files} audio files moved to '{destination_folder}/'")
