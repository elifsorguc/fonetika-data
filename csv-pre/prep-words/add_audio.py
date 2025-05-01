import pandas as pd
import json

# === Step 1: Load input.csv to map words → audio paths ===
audio_df = pd.read_csv("input.csv")

# Safely build the audio path dictionary
audio_dict = {
    str(row["word"]).strip().lower(): row["audio_file"]
    for _, row in audio_df.iterrows()
    if pd.notna(row["word"]) and pd.notna(row["audio_file"])
}

# === Step 2: Load JSON ===
with open("missing_words_to_add.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

# === Step 3: Update audioPath in JSON if a match is found ===
not_found = []

for entry in json_data:
    word = entry["word"].strip().lower()
    if word in audio_dict:
        entry["audioPath"] = audio_dict[word]
    else:
        not_found.append(word)

# === Step 4: Save updated JSON ===
with open("missing_words_updated.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)

print(f"✅ Audio paths updated. {len(not_found)} words were not found in input.csv.")

# Optional: show or save not found list
if not_found:
    print("❌ Words not found:")
    for w in not_found:
        print("-", w)
