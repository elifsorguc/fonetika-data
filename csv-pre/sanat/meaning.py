import json
import pandas as pd

# Load the JSON file
with open('words.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Load the meaning CSV
meaning_df = pd.read_csv('mean.csv')

# Normalize words to lowercase for matching
meaning_dict = dict(zip(meaning_df['word'].str.lower().str.strip(), meaning_df['meaning']))

# Enrich JSON with meanings
for entry in json_data:
    word_lower = entry['word'].lower().strip()
    entry['meaning'] = meaning_dict.get(word_lower, "")

# Save the enriched JSON
with open('last.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)
