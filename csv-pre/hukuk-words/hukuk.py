import csv
import re

def extract_entries(input_file, output_file):
    entries = []
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            # Try to split using a tab character
            if '\t' in line:
                word, meaning = line.split('\t', 1)
            else:
                # Fallback: split based on second capital letter
                matches = list(re.finditer(r'\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\b', line))
                if len(matches) >= 2:
                    second_cap_index = matches[1].start()
                    word = line[:second_cap_index].strip()
                    meaning = line[second_cap_index:].strip()
                else:
                    # If only one capital word, treat first word as word and rest as meaning
                    parts = line.split(' ', 1)
                    word = parts[0]
                    meaning = parts[1] if len(parts) > 1 else ''

            entries.append((word, meaning))

    # Write to CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['word', 'meaning'])
        writer.writerows(entries)

# Usage
extract_entries('hukuk.txt', 'hukuk-mean.csv')
