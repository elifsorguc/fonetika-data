import csv

# Paths
csv_file = "/Users/habibeyilmaz/Desktop/BİTİRME/fixed_fonetika_dataset.csv"
dict_file = "/Users/habibeyilmaz/Documents/MFA/pretrained_models/dictionary/turkish_mfa.dict"

# Convert CSV to MFA dictionary format
with open(csv_file, "r", encoding="utf-8") as infile, open(dict_file, "w", encoding="utf-8") as outfile:
    reader = csv.reader(infile)
    next(reader)  # Skip header row
    for row in reader:
        word, ipa = row
        outfile.write(f"{word} {ipa}\n")

print(f"✅ MFA dictionary saved to {dict_file}")
