import os

# File paths
oov_words_file = "oovs_found.txt"
corpus_dir = "corpus"

# Read OOV words
with open(oov_words_file, "r", encoding="utf-8") as f:
    oov_words = set(f.read().strip().split("\n"))

print(f"🔍 Found {len(oov_words)} OOV words.")

# Check which .lab files contain OOV words
oov_lab_files = []
for file in os.listdir(corpus_dir):
    if file.endswith(".lab"):
        file_path = os.path.join(corpus_dir, file)
        
        # Read .lab file to check its content
        with open(file_path, "r", encoding="utf-8") as f:
            words = f.read().strip().split("\n")

        # If any word in the .lab file is in OOV list, mark it
        if any(word in oov_words for word in words):
            oov_lab_files.append(file)
            print(f"❌ OOV found in: {file} → {words}")

print(f"\n🚀 Total .lab files containing OOV words: {len(oov_lab_files)}")
