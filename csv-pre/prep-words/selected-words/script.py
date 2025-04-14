import pandas as pd
import pdfplumber

# === Step 1: Read the CSV ===
csv_path = 'no_duplicates.csv'  # Replace with your actual CSV path
df = pd.read_csv(csv_path, header=None, names=['word', 'phonetic', 'link'])

# === Step 2: Read and extract all text from the PDF ===
pdf_path = 'input.pdf'  # Replace with your actual PDF path
all_text = ""

print("Reading PDF...")
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        page_text = page.extract_text()
        if page_text:
            all_text += page_text + " "
        print(f"Processed page {i+1}/{len(pdf.pages)}", end='\r')

# Convert PDF text into a set of lowercase words
pdf_words = set(word.strip('.,;:!?()"\'').lower() for word in all_text.split())

# === Step 3: Filter the CSV based on presence in PDF ===
df['word_lower'] = df['word'].str.lower()
filtered_df = df[df['word_lower'].isin(pdf_words)]

# === Step 4: Save the result ===
output_path = 'filtered_output_2.csv'
filtered_df[['word', 'phonetic', 'link']].to_csv(output_path, index=False, header=False)
print(f"\nFiltered CSV saved to {output_path}")
