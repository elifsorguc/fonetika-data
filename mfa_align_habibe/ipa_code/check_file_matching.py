import os

wav_dir = "/Users/habibeyilmaz/Desktop/BİTİRME/mfa_dataset/wav/"
lab_dir = "/Users/habibeyilmaz/Desktop/BİTİRME/mfa_dataset/lab/"

wav_files = {f.replace(".wav", "") for f in os.listdir(wav_dir) if f.endswith(".wav")}
lab_files = {f.replace(".txt", "") for f in os.listdir(lab_dir) if f.endswith(".txt")}

missing_text_files = wav_files - lab_files
missing_wav_files = lab_files - wav_files

if missing_text_files:
    print("❌ Missing text files for:", missing_text_files)
if missing_wav_files:
    print("❌ Missing audio files for:", missing_wav_files)
if not missing_text_files and not missing_wav_files:
    print("✅ All files are correctly matched.")
