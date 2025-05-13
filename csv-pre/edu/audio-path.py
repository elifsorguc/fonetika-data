import pandas as pd

# Load files
all_words_df = pd.read_csv('all-words-filtered.csv')
input_df = pd.read_csv('rtuk-audios.csv')

# Normalize words to lowercase for matching
all_words_df['word_lower'] = all_words_df['word'].str.lower().str.strip()
input_df['word_lower'] = input_df['word'].str.lower().str.strip()

# Merge to get new audio_file values
merged_df = all_words_df.merge(
    input_df[['word_lower', 'audio_file']],
    on='word_lower',
    how='left',
    suffixes=('', '_new')
)

# Update audio_file where a new one is found
merged_df['audio_file'] = merged_df['audio_file_new'].combine_first(merged_df['audio_file'])

# Drop helper columns
merged_df = merged_df.drop(columns=['word_lower', 'audio_file_new'])

# Save updated file
merged_df.to_csv('words-audio-updated.csv', index=False)
