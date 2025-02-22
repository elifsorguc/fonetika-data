import os
import glob

# 📌 Yollar
lab_folder = os.path.expanduser("~/MFA_project/mfa_dataset/lab")
dict_file = os.path.expanduser("~/MFA_project/mfa_dataset/dictionary.dict")

# 📌 DICT'teki kelimeleri oku ve sakla
dict_words = {}
with open(dict_file, "r", encoding="utf-8") as df:
    for line in df:
        parts = line.strip().split()
        if len(parts) > 1:
            word = parts[0]  # İlk kısım kelime
            dict_words[word.lower()] = word  # Küçük harf normalizasyonu ile sakla

# 📌 LAB dosyalarındaki kelimeleri kontrol et ve düzelt
for lab_path in glob.glob(os.path.join(lab_folder, "*.lab")):
    with open(lab_path, "r", encoding="utf-8") as lf:
        content = lf.read().strip()
        words = content.split()  # LAB içindeki kelimeler

    new_words = []
    modified = False
    for word in words:
        lower_word = word.lower()  # Küçük harf normalizasyonu yap
        if lower_word in dict_words and word != dict_words[lower_word]:  
            print(f"{word} -> {dict_words[lower_word]} olarak değiştirildi ({lab_path})")
            new_words.append(dict_words[lower_word])
            modified = True
        else:
            new_words.append(word)

    # 📌 Değişiklik yapıldıysa LAB dosyasını güncelle
    if modified:
        with open(lab_path, "w", encoding="utf-8") as lf:
            lf.write(" ".join(new_words))
        print(f"✔️ LAB dosyası güncellendi: {lab_path}")
