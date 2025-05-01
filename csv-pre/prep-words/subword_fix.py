import pandas as pd
import json

# === Step 1: Load detailed.csv ===
df = pd.read_csv("detailed.csv")
df["word"] = df["word"].str.strip().str.lower()

# === Step 2: Load output.json ===
with open("output.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

# === Step 3: Update matching JSON entries ===
for entry in json_data:
    word = entry["word"].strip().lower()

    # Check if this word is in detailed.csv
    match = df[df["word"] == word]
    if not match.empty:
        row = match.iloc[0]

        # Parse and update values
        subword_list = row["subword_ipas"].split(",")
        vowel_list = row["vowel_ipas"].split(",")

        entry["subword"] = "-".join(subword_list)
        entry["subwordIpa"] = "-".join(subword_list)
        entry["phonemes"] = vowel_list

    # Remove MFCC and formant fields if present
    for key in ["mfcc1", "mfcc2", "mfcc3", "f0", "f1", "f2", "f3"]:
        entry.pop(key, None)

# === Step 4: Save the updated JSON ===
with open("updated_output.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)

print("✅ output.json updated and saved as updated_output.json")
