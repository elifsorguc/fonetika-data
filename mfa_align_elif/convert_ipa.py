# Türkçenin 29 harfini MFA modelinin IPA fonemleri ile eşleştirme
turkish_to_mfa = {
    "a": "a", "b": "b", "c": "dʒ", "ç": "tʃ", "d": "d̪",
    "e": "e", "f": "f", "g": "ɡ", "ğ": "ɡ", "h": "h",
    "ı": "ɯ", "i": "i", "j": "ʒ", "k": "k", "l": "ɫ",
    "m": "m", "n": "n̪", "o": "o", "ö": "œ", "p": "p",
    "r": "ɾ", "s": "s̪", "ş": "ʃ", "t": "t̪", "u": "u",
    "ü": "y", "v": "v", "y": "j", "z": "z̪"
}

# Dosya yolları
input_dict_file = "turkish_dict.txt"
output_dict_file = "dict_ipa.txt"

# Dosyayı aç ve dönüştür
with open(input_dict_file, "r", encoding="utf-8") as infile, open(output_dict_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        parts = line.strip().split()
        if len(parts) > 1:
            word = parts[0]  # Kelime
            transcription = parts[1:]  # Fonemler

            # Her harfi MFA modelinin tanıdığı IPA fonemlerine çevir
            corrected_phonemes = [turkish_to_mfa.get(char, char) for char in transcription]

            # Yeni dosyaya yaz
            outfile.write(f"{word} {' '.join(corrected_phonemes)}\n")

print("Sözlük güncellendi ve MFA modeline uygun hale getirildi. Yeni dosya: turkish_dict_fixed.txt")