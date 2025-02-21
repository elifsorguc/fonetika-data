import os
from collections import Counter

wav_dir = "/Users/habibeyilmaz/Desktop/BİTİRME/mfa_dataset/wav/"
lab_dir = "/Users/habibeyilmaz/Desktop/BİTİRME/mfa_dataset/lab/"

# Get file names without extensions
wav_files = [f.replace(".wav", "") for f in os.listdir(wav_dir) if f.endswith(".wav")]
lab_files = [f.replace(".txt", "") for f in os.listdir(lab_dir) if f.endswith(".txt")]

# Count occurrences
wav_counts = Counter(wav_files)
lab_counts = Counter(lab_files)

# Find missing files
missing_text_files = set(wav_counts.keys()) - set(lab_counts.keys())
missing_wav_files = set(lab_counts.keys()) - set(wav_counts.keys())

# Find words with multiple transcriptions but only one audio file
mismatched_files = {word for word, count in lab_counts.items() if count > 1 and wav_counts.get(word, 0) < count}

# Report
if missing_text_files:
    print("❌ Missing text files for:", missing_text_files)
if missing_wav_files:
    print("❌ Missing audio files for:", missing_wav_files)
if mismatched_files:
    print("⚠️ Possible mismatch: These words have multiple transcriptions but fewer audio files:", mismatched_files)

if not (missing_text_files or missing_wav_files or mismatched_files):
    print("✅ All files are correctly matched.")
