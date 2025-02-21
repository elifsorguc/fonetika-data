import os

# Paths
turkish_dict_path = "turkish_dict.txt"
corpus_dir = "corpus"

# Load words from .lab files
existing_words = set()
for file in os.listdir(corpus_dir):
    if file.endswith(".lab"):
        with open(os.path.join(corpus_dir, file), "r", encoding="utf-8") as f:
            existing_words.update(f.read().split())

# Load dictionary
with open(turkish_dict_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Keep only words that exist in corpus
filtered_dict = []
for line in lines:
    word = line.split()[0]  # Extract the word before phonemes
    if word in existing_words:
        filtered_dict.append(line)

# Write updated dictionary
with open(turkish_dict_path, "w", encoding="utf-8") as f:
    f.writelines(filtered_dict)

print("✅ Updated turkish_dict.txt")
