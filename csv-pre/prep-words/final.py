import json

# Load the JSON file
with open('final_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Turkish vowels
turkish_vowels = ["a", "e", "ı", "i", "o", "ö", "u", "ü"]

def smart_turkish_lower(entry):
    word = entry["word"]
    phonemes = entry.get("phonemes", [])

    if not phonemes or len(word) == 0:
        return word.lower()

    first_phoneme = phonemes[0]

    # Correct the first letter using the vowel if needed
    if first_phoneme in turkish_vowels:
        word = first_phoneme + word[1:]

    # Lowercase rest with Turkish logic
    word = word[0] + word[1:].replace("I", "ı").replace("İ", "i").lower()
    return word

# Apply updates to each entry
for entry in data:
    entry["word"] = smart_turkish_lower(entry)

    # Remove courseId if it exists
    if "courseId" in entry:
        del entry["courseId"]

# Save cleaned JSON
with open('final_output_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Word first letters fixed and 'courseId' removed.")
print("✅ Cleaned file saved as 'final_output_cleaned.json'")
