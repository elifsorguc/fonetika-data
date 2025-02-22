import os
import zipfile
import shutil
import glob

def normalize_turkish(text):
    # Force lowercase and replace Turkish characters and special symbols
    text = text.lower()
    replacements = {
        "ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u",
        "â": "a", "î": "i", "û": "u",
        "-": "_", " ": "_", "'": "_", "’": "_", "‘": "_"
    }
    for turkish_char, ascii_char in replacements.items():
        text = text.replace(turkish_char, ascii_char)
    return text

# Set paths
zip_path = "audios.zip"
audio_folder = "audio_files"
lab_folder = "lab_files"

# Step 1: Unzip audio files into audio_files folder
if os.path.exists(audio_folder):
    shutil.rmtree(audio_folder)
os.makedirs(audio_folder, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(audio_folder)

# Step 2: Normalize filenames in audio_files
audio_files = glob.glob(os.path.join(audio_folder, "*.wav"))
# Store list before renaming
for audio_file in audio_files:
    base = os.path.basename(audio_file)
    name, ext = os.path.splitext(base)
    normalized_name = normalize_turkish(name)
    new_path = os.path.join(audio_folder, normalized_name + ext)
    # If the normalized file already exists, remove this duplicate
    if os.path.exists(new_path) and audio_file != new_path:
        os.remove(audio_file)
    elif audio_file != new_path:
        try:
            os.rename(audio_file, new_path)
        except FileNotFoundError:
            # If the file was already renamed/removed, skip it
            pass

# Step 3: Normalize filenames in lab_files
lab_files = glob.glob(os.path.join(lab_folder, "*.lab"))
for lab_file in lab_files:
    base = os.path.basename(lab_file)
    name, ext = os.path.splitext(base)
    normalized_name = normalize_turkish(name)
    new_path = os.path.join(lab_folder, normalized_name + ext)
    if os.path.exists(new_path) and lab_file != new_path:
        os.remove(lab_file)
    elif lab_file != new_path:
        try:
            os.rename(lab_file, new_path)
        except FileNotFoundError:
            pass

# Step 4: Remove unmatched files from the source folders
# Get normalized names (without extension)
audio_names = {os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(audio_folder, "*.wav"))}
lab_names   = {os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(lab_folder, "*.lab"))}

removed_audio = []
for name in audio_names:
    if name not in lab_names:
        path_to_remove = os.path.join(audio_folder, f"{name}.wav")
        if os.path.exists(path_to_remove):
            os.remove(path_to_remove)
            removed_audio.append(name)

removed_lab = []
for name in lab_names:
    if name not in audio_names:
        path_to_remove = os.path.join(lab_folder, f"{name}.lab")
        if os.path.exists(path_to_remove):
            os.remove(path_to_remove)
            removed_lab.append(name)

# Write removed files info to CSV for reference
with open("removed_unmatched_files.csv", "w", encoding="utf-8") as f:
    f.write("Removed Audio Files:\n")
    for name in removed_audio:
        f.write(name + "\n")
    f.write("\nRemoved Lab Files:\n")
    for name in removed_lab:
        f.write(name + "\n")

print(f"Removed {len(removed_audio)} unmatched audio files and {len(removed_lab)} unmatched lab files.")
print("All filenames in audio_files and lab_files are now normalized and matched.")