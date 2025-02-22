import os
import shutil
import glob

def normalize_turkish(text):
    """
    Türkçe karakterleri ASCII'ye çevirir ve özel karakterleri temizler.
    """
    text = text.lower()
    replacements = {
        "ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u",
        "â": "a", "î": "i", "û": "u",
        "-": "_", " ": "_", "'": "_", "’": "_", "‘": "_"
    }
    for turkish_char, ascii_char in replacements.items():
        text = text.replace(turkish_char, ascii_char)
    return text

# Klasör yolları
wav_folder = os.path.expanduser("~/MFA_project/mfa_dataset/wav_converted")
lab_folder = os.path.expanduser("~/MFA_project/mfa_dataset/lab")
unmatched_folder = os.path.expanduser("~/MFA_project/mfa_dataset/unmatched_files")

# Eğer unmatched_files klasörü yoksa oluştur
os.makedirs(unmatched_folder, exist_ok=True)

# 1️⃣ **Wav ve lab dosyalarının isimlerini normalize et**
for folder, ext in [(wav_folder, ".wav"), (lab_folder, ".lab")]:
    files = glob.glob(os.path.join(folder, f"*{ext}"))
    for file in files:
        base = os.path.basename(file)
        name, extension = os.path.splitext(base)
        normalized_name = normalize_turkish(name) + extension
        new_path = os.path.join(folder, normalized_name)

        if file != new_path:
            os.rename(file, new_path)  # İsmi değiştir

# 2️⃣ **Eşleşmeyen dosyaları bul**
wav_files = {os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(wav_folder, "*.wav"))}
lab_files = {os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(lab_folder, "*.lab"))}

unmatched_wavs = wav_files - lab_files  # Lab karşılığı olmayan wav dosyaları
unmatched_labs = lab_files - wav_files  # Wav karşılığı olmayan lab dosyaları

# 3️⃣ **Eşleşmeyenleri başka bir klasöre taşı**
for name in unmatched_wavs:
    file_path = os.path.join(wav_folder, f"{name}.wav")
    if os.path.exists(file_path):
        shutil.move(file_path, os.path.join(unmatched_folder, f"{name}.wav"))

for name in unmatched_labs:
    file_path = os.path.join(lab_folder, f"{name}.lab")
    if os.path.exists(file_path):
        shutil.move(file_path, os.path.join(unmatched_folder, f"{name}.lab"))

print(f"✅ {len(unmatched_wavs)} wav dosyası ve {len(unmatched_labs)} lab dosyası unmatched_files klasörüne taşındı.")
