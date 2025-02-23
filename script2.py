import pandas as pd

# Load the alignment results CSV
csv_file = "alignment_validation_results.csv"  # Update the file path if needed
df = pd.read_csv(csv_file)

# Count correct and misaligned alignments
total_files = len(df)
correct_alignments = len(df[df["Status"] == "Correct"])
misaligned_alignments = len(df[df["Status"] == "Misaligned"])

# Print the summary
print(f"Total files processed: {total_files}")
print(f"Correctly aligned files: {correct_alignments} ({(correct_alignments / total_files) * 100:.2f}%)")
print(f"Misaligned files: {misaligned_alignments} ({(misaligned_alignments / total_files) * 100:.2f}%)")