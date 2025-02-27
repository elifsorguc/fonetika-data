import os
import textgrid
import csv

# Paths
textgrid_folder = "output"
output_csv = "mfa_dataset.csv"

# Function to parse TextGrid and extract phonemes
def parse_textgrid(file_path):
    tg = textgrid.TextGrid()
    tg.read(file_path)
    
    phonemes = []
    for tier in tg:
        for interval in tier.intervals:
            if interval.mark.strip():
                phonemes.append(interval.mark.strip())  # Extract phoneme text
    
    return " ".join(phonemes)  # Join phonemes into a sequence

# Create CSV file
with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["path", "phonemes"])  # Headers
    
    for file in os.listdir(textgrid_folder):
        if file.endswith(".TextGrid"):
            phonemes = parse_textgrid(os.path.join(textgrid_folder, file))
            audio_path = file.replace(".TextGrid", ".wav")  # Match with audio file
            
            writer.writerow([audio_path, phonemes])

print(f"✅ MFA dataset saved as {output_csv}")
