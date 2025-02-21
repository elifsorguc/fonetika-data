import os
import csv

dataset_file = "dataset.csv"
audio_folder = "corpus"
missing_words_log = "missing_audio.txt"

# Get all existing audio files (convert to a set of numbers for fast lookup)
existing_audio_files = {f.split(".")[0] for f in os.listdir(audio_folder) if f.endswith(".wav")}

missing_words = []

# Read dataset and check for missing files
with open(dataset_file, "r", encoding="utf-8") as infile:
    reader = csv.reader(infile)
    next(reader)  # Skip header

    for row in reader:
        word, _, _, seskelime_number = row  # Extract word and ID
        seskelime_number = seskelime_number.strip()

        if not word.strip():  # Skip rows without words
            continue

        if seskelime_number not in existing_audio_files:  # Check if audio is missing
            missing_words.append(f"{seskelime_number} - {word}")

# Save missing words log
with open(missing_words_log, "w", encoding="utf-8") as f:
    f.write("\n".join(missing_words))

print(f"✅ Done! Missing words saved in {missing_words_log}")
