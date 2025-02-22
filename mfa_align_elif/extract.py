import os
import glob
import re
import pandas as pd

def parse_textgrid(textgrid_path):
    """
    Parses a TextGrid file and extracts word-level alignments.
    Returns:
        - file_name (str): Name of the TextGrid file
        - words (list of tuples): List of (word, start_time, end_time) tuples
    """
    words = []
    with open(textgrid_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    word_tier = False
    current_word = None
    start_time, end_time = None, None

    for i, line in enumerate(lines):
        line = line.strip()

        # Detect the "words" tier
        if 'name = "words"' in line:
            word_tier = True
            continue

        if word_tier:
            if line.startswith("xmin"):
                start_time = float(re.findall(r"[\d.]+", line)[0])
            elif line.startswith("xmax"):
                end_time = float(re.findall(r"[\d.]+", line)[0])
            elif line.startswith("text"):
                match = re.findall(r'"(.*?)"', line)
                current_word = match[0] if match else ""

                # Add word entry if it's non-empty
                if current_word.strip():
                    words.append((current_word, start_time, end_time))

            # End of words tier
            if line.startswith("item [2]:"):
                break

    return os.path.basename(textgrid_path), words

def analyze_textgrid_directory(textgrid_dir):
    """
    Analyzes all TextGrid files in a directory.
    """
    textgrid_files = glob.glob(os.path.join(textgrid_dir, "*.TextGrid"))
    total_files = len(textgrid_files)
    aligned_words = 0
    empty_intervals = 0
    results = []

    for textgrid_file in textgrid_files:
        file_name, words = parse_textgrid(textgrid_file)
        num_words = len(words)
        
        if num_words > 0:
            aligned_words += num_words
        else:
            empty_intervals += 1  # Track files with no words
        
        results.append({"file": file_name, "num_words": num_words})

    # Convert results to a DataFrame
    df = pd.DataFrame(results)
    
    # Print Summary
    print(f"\n📌 **TextGrid Analysis Summary** 📌")
    print(f"Total TextGrid files analyzed: {total_files}")
    print(f"Files with aligned words: {total_files - empty_intervals}")
    print(f"Files with empty alignments: {empty_intervals}")
    print(f"Total aligned words: {aligned_words}")

    # Save the summary as a CSV file
    output_csv = "alignment_summary.csv"
    df.to_csv(output_csv, index=False)
    print(f"📄 Alignment report saved to: {output_csv}")

# Set the path to the folder containing TextGrid files
textgrid_directory = "output"  # Change to your directory name
analyze_textgrid_directory(textgrid_directory)
