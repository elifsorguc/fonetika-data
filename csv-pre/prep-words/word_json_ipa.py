import pandas as pd
import json

# Read CSV
df = pd.read_csv("words-output.csv")

# Create list of JSON entries
entries = []

for _, row in df.iterrows():
    entry = {
        "word": row["word"],
        "subword": "",
        "subwordIpa": "",
        "phoneticWriting": row["phonetic"],
        "phonemes": [],
        "audioPath": row["audio_file"],
        "mfcc1": None,
        "mfcc2": None,
        "mfcc3": None,
        "f0": None,
        "f1": None,
        "f2": None,
        "f3": None
    }
    entries.append(entry)

# Save to JSON file
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(entries, f, indent=2, ensure_ascii=False)

print("✅ output.json generated successfully.")
