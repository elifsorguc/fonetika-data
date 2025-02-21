import re

# Define the phoneme-to-IPA mapping
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
    ":": 'ː',  # Vurgu (lengthening)
}

# Function to attach lengthening markers to vowels
def fix_ipa_format(ipa_transcription):
    """
    Fixes the IPA transcription by attaching lengthening markers to the preceding vowel.
    """
    # Attach "ː" to the preceding vowel
    fixed_ipa = re.sub(r'\sː', 'ː', ipa_transcription)

    return fixed_ipa

# Read and process the dictionary file
input_file = "turkish_dict.txt"
output_file = "turkish_dict_fixed.txt"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        parts = line.strip().split(maxsplit=1)  # Split word and IPA transcription
        if len(parts) == 2:
            word, ipa = parts
            fixed_ipa = fix_ipa_format(ipa)  # Fix the IPA transcription
            outfile.write(f"{word} {fixed_ipa}\n")
        else:
            outfile.write(line)  # If the line is invalid, keep it as is

print(f"Fixed dictionary saved as {output_file}")
