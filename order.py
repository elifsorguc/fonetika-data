import csv
import re

def extract_number(url):
    """Extracts the number after 'SesKelime/' in the URL."""
    match = re.search(r'/SesKelime/(\d+)', url)
    return int(match.group(1)) if match else float('inf')

def sort_and_fill_csv(input_file, output_file):
    """Sorts CSV rows by the number extracted from the audio_file column and fills missing numbers."""
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read header
        rows = list(reader)
    
    # Extract numbers and sort rows
    extracted_numbers = sorted(set(extract_number(row[2]) for row in rows))
    min_num, max_num = extracted_numbers[0], extracted_numbers[-1]
    
    # Create a dictionary mapping numbers to rows
    row_dict = {extract_number(row[2]): row for row in rows}
    
    # Generate all numbers in range and fill missing ones
    complete_rows = []
    for num in range(min_num, max_num + 1):
        if num in row_dict:
            complete_rows.append(row_dict[num] + [num])
        else:
            complete_rows.append(["", "", f"https://sozluk.rtuk.gov.tr/Home/SesKelime/{num}", num])
    
    # Write to new CSV file
    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header + ["SesKelime Number"])  # Add new column header
        writer.writerows(complete_rows)

# Example usage
input_csv = "input.csv"  # Replace with actual input CSV file
output_csv = "sorted_filled_output.csv"
sort_and_fill_csv(input_csv, output_csv)
print(f"Sorted and filled CSV saved as {output_csv}")