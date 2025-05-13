import pandas as pd
import json

# Load the CSV
df = pd.read_csv('words-audio-updated.csv')

# Function to build JSON object for each row
def build_entry(row):
    return {
        "word": row["word"],
        "subword": row["subword_string"].replace(",", "-"),
        "subwordIpa": row["subword_ipas"].replace(",", "-"),
        "phoneticWriting": row["word_ipa"],
        "phonemes": [v.strip() for v in row["vowel_ipas"].split(",") if v.strip()],
        "audioPath": row["audio_file"]
    }

# Build the list of entries
entries = [build_entry(row) for _, row in df.iterrows()]

# Save to JSON file
with open('words.json', 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)
