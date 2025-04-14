import pandas as pd

# Read CSV
csv_path = 'filtered_output.csv'  # Replace with your file name
df = pd.read_csv(csv_path, header=None, names=['word', 'phonetic', 'link'])

# Count exact word duplicates
duplicates = df[df.duplicated(subset=['word'], keep=False)]

print(f"Total exact duplicate rows found: {len(duplicates)}")

# Drop exact duplicates but keep first occurrence
df_unique = df.drop_duplicates(subset=['word'], keep='first')

# Save cleaned file
output_path = 'output.csv'
df_unique.to_csv(output_path, index=False, header=False)

print(f"Cleaned file saved to: {output_path}")
