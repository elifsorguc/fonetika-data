import os
import textgrid
import csv

# Paths
textgrid_folder = "test-output"  # Change this to your TextGrid folder
output_csv = "test-mfa.csv"

# Function to extract words & phoneme timestamps
def parse_textgrid(file_path):
    tg = textgrid.TextGrid()
    tg.read(file_path)

    words = []
    phonemes = []
    timestamps = []

    for tier in tg:
        if tier.name.lower() == "words":  # Extract words
            for interval in tier.intervals:
                if interval.mark.strip():  # Use `mark` instead of `text`
                    words.append(interval.mark.strip())

        elif tier.name.lower() == "phones":  # Extract phonemes & timestamps
            for interval in tier.intervals:
                if interval.mark.strip():  # Ignore empty intervals
                    phonemes.append(interval.mark.strip())
                    timestamps.append((interval.minTime, interval.maxTime))

    return " ".join(words), " ".join(phonemes), timestamps

# Create CSV file
with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["audio_path", "words", "phonemes", "timestamps"])  # Headers
    
    for file in os.listdir(textgrid_folder):
        if file.endswith(".TextGrid"):
            words, phonemes, timestamps = parse_textgrid(os.path.join(textgrid_folder, file))
            audio_path = file.replace(".TextGrid", ".wav")  # Match with audio file
            
            writer.writerow([audio_path, words, phonemes, timestamps])

print(f"✅ Fixed! Dataset saved as {output_csv}")
