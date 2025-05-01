import pandas as pd

# === Step 1: List of target words ===
target_words = [
    "dermek", "poster", "amber", "halter", "diyetisyen", "personel", "söğüt", "şöbiyet", "ömür", "çöl", "övünmek",
    "görkem", "öğle", "asansör", "yönetim", "külah", "selam", "bilakis", "ilan", "şelale", "bilardo", "muallak",
    "selanik", "telaş", "şarkı", "bostancı", "penaltı", "gıda", "ıtır", "nakış", "kılıbık", "horon", "boykot",
    "ordu", "doğru", "kudüs", "öksürük", "külüstür", "omuz", "yumurcak", "kurulu"
]

# Normalize (lowercase and strip)
target_words = [w.strip().lower() for w in target_words]

# === Step 2: Load CSV ===
df = pd.read_csv("detailed.csv")

# Normalize the 'word' column
df["word"] = df["word"].str.strip().str.lower()

# === Step 3: Filter for matching words ===
filtered_df = df[df["word"].isin(target_words)]

# === Step 4: Save to new CSV ===
filtered_df.to_csv("filtered_words.csv", index=False)

print(f"✅ Found and saved {len(filtered_df)} matching rows to 'filtered_words.csv'")
