# Define input and output file names
input_file = "turkish_dict.txt"
output_file = "turkish_dict_cleaned.txt"

# Read the file and clean the quotes
with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        cleaned_line = line.replace('"', '')  # Remove double quotes
        outfile.write(cleaned_line)

print(f"Cleaned dictionary saved as {output_file}")
