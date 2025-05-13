import pandas as pd

# Load both CSVs
all_words_df = pd.read_csv('all-words.csv')
hukuk_df = pd.read_csv('hukuk-mean.csv')

# Normalize word columns to lowercase for comparison
all_words_df['word_lower'] = all_words_df['word'].str.lower().str.strip()
hukuk_words_set = set(hukuk_df['word'].str.lower().str.strip())

# Filter rows where word exists in hukuk list
filtered_df = all_words_df[all_words_df['word_lower'].isin(hukuk_words_set)]

# Drop the helper column
filtered_df = filtered_df.drop(columns=['word_lower'])

# Save filtered results
filtered_df.to_csv('all-words-filtered.csv', index=False)
