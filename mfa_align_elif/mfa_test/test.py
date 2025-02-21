import csv
import os
import re

# Phoneme-to-IPA mapping
phoneme_to_ipa = {
    'a': 'a', 'â': 'ɑ', 'e': 'ɛ', 'é': 'e', 'ı': 'ɯ', 'i': 'i',
    'o': 'o', 'ô': 'oː', 'u': 'u', 'û': 'uː', 'ü': 'y', 'ö': 'œ',
    'b': 'b', 'c': 'd͡ʒ', 'ç': 't͡ʃ', 'd': 'd', 'f': 'f', 'g': 'ɡ',
    'ğ': '', 'h': 'h', 'j': 'ʒ', 'm': 'm', 'n': 'n', 'ñ': 'ŋ',
    'p': 'p', 'r': 'ɾ', 's': 's', 'ş': 'ʃ', 'v': 'v', 'y': 'j',
    'z': 'z', 'A': 'a', 'Â': 'aː', 'E': 'ɛ', 'É': 'e', 'I': 'ɯ', 'İ': 'i',
    'O': 'o', 'Ô': 'oː', 'U': 'u', 'Û': 'uː', 'Ü': 'y', 'Ö': 'œ',
    'B': 'b', 'C': 'd͡ʒ', 'Ç': 't͡ʃ', 'D': 'd', 'F': 'f', 'G': 'ɡ',
    'Ğ': '', 'H': 'h', 'J': 'ʒ', 'M': 'm', 'N': 'n',
    'P': 'p', 'R': 'ɾ', 'S': 's', 'Ş': 'ʃ', 'V': 'v', 'Y': 'j',
    'Z': 'z', 't': 't', 'T': 't'
}

# Mapping for signs
sign_to_ipa = {
    "~": '‿',  # Ulama (linking)
    "⁓": '‿',
    "‿": '‿',
    ":": 'ː'   # Vurgu (lengthening)
}

# Convert phonetic notation to IPA with spaces between phonemes
def phonetic_to_ipa(phonetic):
    phonetic = phonetic.strip()
    ipa_word = []
    
    for char in phonetic:
        if char in sign_to_ipa:
            ipa_word.append(sign_to_ipa[char])
        elif char in phoneme_to_ipa:
            ipa_word.append(phoneme_to_ipa[char])
        else:
            ipa_word.append(char)  # Keep unknown characters
    
    return " ".join(ipa_word)  # Space-separated phonemes

# Paths
dataset_path = "dataset.csv"
output_dict_path = "turkish_dict_2.txt"
corpus_dir = "corpus"

# Ensure corpus directory exists
os.makedirs(corpus_dir, exist_ok=True)

# Process CSV and create turkish_dict.txt + .lab files
with open(dataset_path, "r", encoding="utf-8") as infile, \
     open(output_dict_path, "w", encoding="utf-8") as dict_file:
    
    reader = csv.DictReader(infile)
    for row in reader:
        word = row["word"].strip()
        phonetic = row["phonetic"].strip()
        seskelime_number = row["SesKelime Number"].strip()

        # Skip empty words or phonetics
        if not word or not phonetic or not seskelime_number:
            continue

        # Convert phonetics to IPA
        ipa_representation = phonetic_to_ipa(phonetic)

        # Write to turkish_dict.txt
        dict_file.write(f"{word} {ipa_representation}\n")

        # Create .lab file for alignment
        lab_path = os.path.join(corpus_dir, f"{seskelime_number}.lab")
        with open(lab_path, "w", encoding="utf-8") as lab_file:
            lab_file.write(word + "\n")

print("✅ Processing complete! `turkish_dict.txt` and `.lab` files are created.")
