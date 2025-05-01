import json

# Load the JSON file
with open("updated_output.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

# Find entries with missing or empty subword
missing_subword_words = [entry["word"] for entry in json_data if not entry.get("subword")]

# Print the results
if missing_subword_words:
    print("❌ Words with missing subword fields:")
    for word in missing_subword_words:
        print("-", word)
else:
    print("✅ All entries have a subword!")

# Optional: save to a .txt file
with open("missing_subwords.txt", "w", encoding="utf-8") as f:
    for word in missing_subword_words:
        f.write(word + "\n")
