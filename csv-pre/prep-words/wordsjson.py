import pandas as pd
import json

# Load the original CSV
df = pd.read_csv('words-output.csv', header=None, names=['word', 'phonetic', 'audio_url'])

structured_data = []

def dummy_ipa(word):
    return word.lower().replace("a", "ɑ").replace("e", "ɛ")

def dummy_phonemes(word):
    return list(word.lower())

# Process each word row
for _, row in df.iterrows():
    word = row['word'].capitalize()
    phonetic = row['phonetic']
    audio_url = row['audio_url']
    word_lower = word.lower()

    entry = {
        "word": word,
        "subword": '-'.join([word[:len(word)//2], word[len(word)//2:]]),  # naive split
        "subwordIpa": '-'.join([dummy_ipa(word[:len(word)//2]), dummy_ipa(word[len(word)//2:])]),
        "phoneticWriting": dummy_ipa(word).replace("-", "."),
        "phonemes": dummy_phonemes(word),
        "audioPath": audio_url,
        "courseId": "course_01",
        "mfcc1": 0.7,
        "mfcc2": -0.9,
        "mfcc3": 1.1,
        "f0": 112,
        "f1": 680,
        "f2": 1350,
        "f3": 2450
    }
    structured_data.append(entry)

# Save final output as JSON
with open('final_output.json', 'w', encoding='utf-8') as f:
    json.dump(structured_data, f, ensure_ascii=False, indent=2)

print("✅ Final structured data saved to: final_output.json")
