import pandas as pd
import json

# === Step 1: Load CSV and JSON ===
csv_df = pd.read_csv("filtered_words.csv")
with open("filtered_output.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

# === Step 2: Build set of existing words ===
existing_words = {entry["word"].strip().lower() for entry in json_data}

# === Step 3: Find and build missing entries ===
new_entries = []

for _, row in csv_df.iterrows():
    word = row["word"].strip().lower()
    if word not in existing_words:
        subword_list = row["subword_ipas"].split(",")
        vowel_list = row["vowel_ipas"].split(",")

        new_entry = {
            "word": word,
            "subword": "-".join(subword_list),
            "subwordIpa": "-".join(subword_list),
            "phoneticWriting": row["word_ipa"],
            "phonemes": vowel_list,
            "audioPath": f"https://sozluk.rtuk.gov.tr/Home/SesKelime/UNKNOWN"
        }

        new_entries.append(new_entry)

# === Step 4: Save missing words to a new JSON ===
with open("missing_words_to_add.json", "w", encoding="utf-8") as f:
    json.dump(new_entries, f, indent=2, ensure_ascii=False)

print(f"✅ Created 'missing_words_to_add.json' with {len(new_entries)} new entries.")
