import pandas as pd
import pdfplumber
import os

# === Step 1: Read the CSV ===
df = pd.read_csv('input.csv', header=None, names=['word', 'phonetic', 'link'])

# === Step 2: Define all your PDF paths ===
pdf_paths = [f"input{i}.pdf" for i in range(1, 8)]

# === Step 3: Extract words from all PDFs ===
pdf_words = set()

print("Reading PDFs...")
for i, pdf_path in enumerate(pdf_paths):
    if not os.path.exists(pdf_path):
        print(f"⚠️ Skipping missing PDF: {pdf_path}")
        continue
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                words = text.split()
                pdf_words.update(word.strip('.,;:!?()"\'').lower() for word in words)
    print(f"✓ Processed {pdf_path} ({i+1}/7)")

# === Step 4: Extract words from TXT ===
txt_words = set()
txt_path = 'input.txt'
if os.path.exists(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        txt_content = f.read()
        txt_words = set(word.strip('.,;:!?()"\'').lower() for word in txt_content.split())
    print("✓ Processed input.txt")
else:
    print("⚠️ TXT file not found, skipping input.txt")

# === Step 5: Merge all found words
all_found_words = pdf_words.union(txt_words)

# === Step 6: Filter the DataFrame
df['word_lower'] = df['word'].str.lower()
filtered_df = df[df['word_lower'].isin(all_found_words)]

# === Step 7: Save result
filtered_df[['word', 'phonetic', 'link']].to_csv('words-output.csv', index=False, header=False)
print(f"\n✅ Done. Filtered CSV saved to: words-output.csv")
