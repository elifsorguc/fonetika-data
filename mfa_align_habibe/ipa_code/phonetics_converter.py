import csv
import re

# Phoneme-to-IPA mapping
phoneme_to_ipa = {
    'a': 'a', 'â': 'ɑ', 'e': 'ɛ', 'é': 'e', 'ı': 'ɯ', 'i': 'i',
    'o': 'o', 'ô': 'oː', 'u': 'u', 'û': 'uː', 'ü': 'y', 'ö': 'œ',
    'b': 'b', 'c': 'd͡ʒ', 'ç': 't͡ʃ', 'd': 'd', 'f': 'f', 'g': 'ɡ',
    'ğ': '', 'h': 'h', 'j': 'ʒ', 'm': 'm', 'n': 'n', 'ñ': 'ŋ',
    'p': 'p', 'r': 'ɾ', 's': 's', 'ş': 'ʃ', 'v': 'v', 'y': 'j',
    'z': 'z','A': 'a', 'Â': 'aː', 'E': 'ɛ', 'É': 'e', 'I': 'ɯ', 'İ': 'i',
    'O': 'o', 'Ô': 'oː', 'U': 'u', 'Û': 'uː', 'Ü': 'y', 'Ö': 'œ',
    'B': 'b', 'C': 'd͡ʒ', 'Ç': 't͡ʃ', 'D': 'd', 'F': 'f', 'G': 'ɡ',
    'Ğ': '', 'H': 'h', 'J': 'ʒ', 'M': 'm', 'N': 'n',
    'P': 'p', 'R': 'ɾ', 'S': 's', 'Ş': 'ʃ', 'V': 'v', 'Y': 'j',
    'Z': 'z', 't': 't', 'T': 't'
}

# Mapping for signs
sign_to_ipa = {
    "~": '‿',    # Ulama (linking)
    "⁓": '‿',
    "‿": '‿',
    ":": 'ː',    # Vurgu (lengthening)
}

# Rules for ğ
def apply_rules(phonetic):
    # Remove text inside parentheses
    phonetic = re.sub(r'\([^)]*\)', '', phonetic).strip()
    
    # If phonetic writing uses ':', lengthen the preceding vowel
    if ':' in phonetic:
        vowel = phonetic.split(':')[0].lower()
        # Escape special characters (unknown characters)
        vowel_escaped = re.escape(vowel)
        phonetic = re.sub(rf'{vowel_escaped}ğ', f'{vowel}ː', phonetic)
    # If phonetic writing uses '~', connect the vowels with '‿'
    elif '~' in phonetic:
        vowels = phonetic.split('~')
        # Escape special characters (unknown characters)
        vowels_escaped = [re.escape(v) for v in vowels]
        phonetic = re.sub(rf'{vowels_escaped[0]}ğ{vowels_escaped[1]}', f'{vowels[0]}‿{vowels[1]}', phonetic)
    # Otherwise, remove ğ
    else:
        phonetic = phonetic.replace('ğ', '')
    return phonetic

# Determine if a vowel is kalın or ince
def is_ince(vowel):
    return vowel in {'e', 'é', 'i', 'â','ö','ü','û','ô'}

# Convert Turkish phonetic to IPA
def phonetic_to_ipa(phonetic):
    phonetic = apply_rules(phonetic)
    ipa_word = []
    i = 0
    while i < len(phonetic):
        char = phonetic[i]
        # Handle signs
        if char in sign_to_ipa:
            ipa_word.append(sign_to_ipa[char])
            i += 1
            continue
        # Handle k, l rules (based on the next vowel only)
        if char in {'k', 'l', 'K', 'L'}:
            # Check the next character to determine if it is an ince vowel
            if i + 1 < len(phonetic):  # Ensure there is a next character
                next_char = phonetic[i + 1]
                if next_char:
                    # If the next character is an ince vowel
                    if char in {'k', 'K'}:
                        ipa_char = 'c' if is_ince(next_char) else 'k'
                    elif char in {'l', 'L'}:
                        ipa_char = 'l' if is_ince(next_char) else 'ɫ'
                    ipa_word.append(ipa_char)
                    i += 1
                    continue
            # If no next vowel or at the end, keep it as is
            ipa_word.append(phoneme_to_ipa.get(char, char))  # Use get method to avoid KeyError
        # Default to phoneme-to-IPA mapping
        elif char in phoneme_to_ipa:
            ipa_word.append(phoneme_to_ipa[char])
        else:
            ipa_word.append(char)  # Keep the character as is if not found
        # Skip unknown characters
        i += 1
    return ''.join(ipa_word)

# Process CSV file
def process_csv(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        # Use semicolon as the delimiter
        reader = csv.DictReader(infile, delimiter=';')
        fieldnames = ['word', 'phonetic', 'ipa', 'audio_file']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for row in reader:
            word = row['word']
            phonetic = row['phonetic']
            audio_file = row['audio_file']
            ipa_word = phonetic_to_ipa(phonetic)
            row['ipa'] = ipa_word
            # Reorder the row to match the desired column order
            writer.writerow({
                'word': word,
                'phonetic': phonetic,
                'ipa': ipa_word,
                'audio_file': audio_file
            })

# Example usage
input_csv = 'scraped_words_dataset.csv'  # Updated file name
output_csv = 'output.csv'
process_csv(input_csv, output_csv)