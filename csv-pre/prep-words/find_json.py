import json

# === Step 1: List of target words ===
target_words = [
    "dermek", "poster", "amber", "halter", "diyetisyen", "personel", "söğüt", "şöbiyet", "ömür", "çöl", "övünmek",
    "görkem", "öğle", "asansör", "yönetim", "külah", "selam", "bilakis", "ilan", "şelale", "bilardo", "muallak",
    "selanik", "telaş", "şarkı", "bostancı", "penaltı", "gıda", "ıtır", "nakış", "kılıbık", "horon", "boykot",
    "ordu", "doğru", "kudüs", "öksürük", "külüstür", "omuz", "yumurcak", "kurulu"
]

# Normalize the word list
target_words = [w.strip().lower() for w in target_words]

# === Step 2: Load JSON ===
with open("filtered_output.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

# === Step 3: Filter JSON entries ===
filtered_entries = [entry for entry in json_data if entry["word"].strip().lower() in target_words]

# === Step 4: Save to new JSON ===
with open("filtered_words_from_json.json", "w", encoding="utf-8") as f:
    json.dump(filtered_entries, f, indent=2, ensure_ascii=False)

print(f"✅ Found and saved {len(filtered_entries)} matching entries to 'filtered_words_from_json.json'")
