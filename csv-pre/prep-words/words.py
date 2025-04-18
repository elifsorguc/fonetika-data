import os
import pandas as pd

# Use the current directory instead of /mnt/data/
upload_path = "."

# Look for CSV files in the current directory
files = os.listdir(upload_path)
csv_files = [f for f in files if f.endswith(".csv")]

# Read the first CSV file found
if csv_files:
    file_path = os.path.join(upload_path, csv_files[0])
    df = pd.read_csv(file_path, header=None)
    words = df[0].tolist()

    # Save the output .txt file in the same directory
    output_txt_path = os.path.join(upload_path, "words_only_from_file.txt")
    with open(output_txt_path, "w", encoding="utf-8") as f:
        for word in words:
            f.write(word + "\n")

    print(f"Words extracted and saved to: {output_txt_path}")
else:
    print("No CSV file found in the current directory.")
