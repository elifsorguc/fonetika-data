import os
import pandas as pd
import textgrid

# Set paths
textgrid_folder = "mfa_align_aysegul/aligned_output"  # Folder containing aligned TextGrid files
dictionary_path = "mfa_align_aysegul/dict/filtered_turkish_dict.txt"  # Turkish dictionary file

# Function to load Turkish dictionary
def load_dictionary(dictionary_path):
    turkish_dict = {}
    with open(dictionary_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            word = parts[0]
            phonemes = parts[1:]
            turkish_dict[word] = phonemes
    return turkish_dict

# Function to parse a TextGrid file
def parse_textgrid(textgrid_path):
    tg = textgrid.TextGrid.fromFile(textgrid_path)
    word_tier, phone_tier = None, None

    for tier in tg.tiers:
        if tier.name.lower() == "words":
            word_tier = tier
        elif tier.name.lower() == "phones":
            phone_tier = tier

    if not word_tier or not phone_tier:
        return None, None

    # Extract words
    word_alignments = [(interval.mark.strip(), float(interval.minTime), float(interval.maxTime)) 
                       for interval in word_tier if interval.mark.strip()]

    # Extract phonemes
    phone_alignments = [(interval.mark.strip(), float(interval.minTime), float(interval.maxTime)) 
                        for interval in phone_tier if interval.mark.strip()]

    return word_alignments, phone_alignments

# Function to validate alignments
def validate_alignments(textgrid_folder, dictionary):
    results = []

    for filename in os.listdir(textgrid_folder):
        if filename.endswith(".TextGrid"):
            tg_path = os.path.join(textgrid_folder, filename)
            word_alignments, phone_alignments = parse_textgrid(tg_path)

            if word_alignments is None or phone_alignments is None:
                results.append([filename, "Error", "Missing word or phoneme tier"])
                continue

            # Compare each word to the dictionary
            mismatched_words = []
            missing_words = []
            for word, start, end in word_alignments:
                if word not in dictionary:
                    missing_words.append(word)
                else:
                    expected_phonemes = dictionary[word]
                    aligned_phonemes = [ph[0] for ph in phone_alignments if start <= ph[1] < end]
                    
                    if aligned_phonemes != expected_phonemes:
                        mismatched_words.append(word)

            if mismatched_words or missing_words:
                results.append([filename, "Misaligned", f"Mismatch: {mismatched_words}, Missing: {missing_words}"])
            else:
                results.append([filename, "Correct", "Aligned properly"])

    return results

# Load dictionary
turkish_dict = load_dictionary(dictionary_path)

# Validate alignments
alignment_results = validate_alignments(textgrid_folder, turkish_dict)

# Convert results to DataFrame
df = pd.DataFrame(alignment_results, columns=["File", "Status", "Details"])

# Save results to CSV
df.to_csv("alignment_validation_results.csv", index=False, encoding="utf-8")

# Display summary
print("Validation complete! Results saved to 'alignment_validation_results.csv'")