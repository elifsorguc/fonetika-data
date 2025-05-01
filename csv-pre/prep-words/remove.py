import json

# === Step 1: Load words to remove from TXT ===
with open("missing_subwords.txt", "r", encoding="utf-8") as f:
    words_to_remove = set(line.strip().lower() for line in f if line.strip())

# === Step 2: Load JSON ===
with open("updated_output.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

# === Step 3: Filter JSON entries ===
filtered_data = [entry for entry in json_data if entry["word"].strip().lower() not in words_to_remove]

# === Step 4: Save the result ===
with open("filtered_output.json", "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, indent=2, ensure_ascii=False)

print(f"✅ Removed {len(json_data) - len(filtered_data)} entries. Saved as filtered_output.json")
