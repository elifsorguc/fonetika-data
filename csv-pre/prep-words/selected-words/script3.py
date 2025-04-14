import pandas as pd
import pdfplumber

# === Step 1: Read the CSV ===
csv_path = 'input.csv'
df = pd.read_csv(csv_path, header=None, names=['word', 'phonetic', 'link'])

# === Step 2: Read PDF words ===
pdf_path = 'input.pdf'
pdf_text = ""

print("Reading PDF...")
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        page_text = page.extract_text()
        if page_text:
            pdf_text += page_text + " "
        print(f"Processed page {i+1}/{len(pdf.pages)}", end='\r')

pdf_words = set(word.strip('.,;:!?()"\'').lower() for word in pdf_text.split())

# === Step 3: Read TXT words ===
txt_path = 'input.txt'
with open(txt_path, 'r', encoding='utf-8') as f:
    txt_content = f.read()

txt_words = set(word.strip('.,;:!?()"\'').lower() for word in txt_content.split())

# === Step 4: Combine PDF + TXT words ===
combined_words = pdf_words.union(txt_words)

# === Step 5: Filter CSV rows ===
df['word_lower'] = df['word'].str.lower()
filtered_df = df[df['word_lower'].isin(combined_words)]

# === Step 6: Save output ===
output_path = 'words.csv'
filtered_df[['word', 'phonetic', 'link']].to_csv(output_path, index=False, header=False)

print(f"\nFiltered CSV saved to: {output_path}")
