import pandas as pd

# Read ipa.csv using semicolon as the delimiter
ipa_df = pd.read_csv("ipa.csv", delimiter=';')

# Read words-output.csv (assumes it's comma-separated)
words_df = pd.read_csv("words-output.csv")

# Create a word → ipa dictionary
ipa_dict = dict(zip(ipa_df['word'], ipa_df['ipa']))

# Update phonetic if word matches
words_df['phonetic'] = words_df.apply(
    lambda row: ipa_dict.get(row['word'], row['phonetic']),
    axis=1
)

# Save the updated file
words_df.to_csv("words-output.csv", index=False)

print("✅ phonetic column updated using ipa.csv")
