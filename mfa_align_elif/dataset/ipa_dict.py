import pandas as pd

# Load dataset
df = pd.read_csv("dataset.csv", sep=";", encoding="utf-8")

# Select relevant columns (word and IPA transcription)
df_filtered = df[["word", "ipa"]]

# Add spaces between IPA letters
df_filtered["ipa_spaced"] = df_filtered["ipa"].apply(lambda x: " ".join(x))

# Save to text file
output_file = "turkish_dict.txt"
df_filtered[["word", "ipa_spaced"]].to_csv(output_file, sep=" ", index=False, header=False, encoding="utf-8")

print(f"Saved processed dictionary to {output_file}")
