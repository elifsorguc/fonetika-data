import pandas as pd

# Load CSV file
file_path = "/Users/habibeyilmaz/Desktop/BİTİRME/fixed_fonetika_dataset.csv"
df = pd.read_csv(file_path)

# Define columns (Update if needed)
word_column = "word"
ipa_column = "ipa"

# Create MFA dictionary format
output_file = "/Users/habibeyilmaz/Documents/MFA/pretrained_models/dictionary/turkish_mfa.dict"

with open(output_file, "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        f.write(f"{row[word_column]}    {row[ipa_column]}\n")

print(f"✅ MFA dictionary created: {output_file}")
