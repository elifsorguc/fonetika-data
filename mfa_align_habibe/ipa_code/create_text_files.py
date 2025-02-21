import csv
import os

# Paths
csv_file = "/Users/habibeyilmaz/Desktop/BİTİRME/fixed_fonetika_dataset.csv"
audio_dir = "/Users/habibeyilmaz/Desktop/BİTİRME/audio_files"
transcriptions_dir = "/Users/habibeyilmaz/Desktop/BİTİRME/text_files"

# Create transcriptions directory if it doesn't exist
os.makedirs(transcriptions_dir, exist_ok=True)

# Read CSV and create transcription files
with open(csv_file, "r", encoding="utf-8") as infile:
    reader = csv.reader(infile)
    next(reader)  # Skip header row
    for row in reader:
        word = row[0]  # Extract word
        txt_file_path = os.path.join(transcriptions_dir, f"{word}.txt")
        with open(txt_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(word)  # Write word (not IPA)

print(f"✅ Transcription files saved in {transcriptions_dir}")
