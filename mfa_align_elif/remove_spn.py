import pandas as pd

# Load the dataset
input_csv = "mfa_dataset_with_timestamps.csv"  # Replace with your actual filename
output_csv = "dataset.csv"

df = pd.read_csv(input_csv)

# Remove rows where "phonemes" contains "spn"
df_cleaned = df[~df["phonemes"].str.contains("spn", na=False)]

# Save the cleaned dataset
df_cleaned.to_csv(output_csv, index=False)

print(f"✅ Cleaned dataset saved as {output_csv}")
