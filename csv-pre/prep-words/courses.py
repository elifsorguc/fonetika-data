import json

# === Step 1: Load your existing JSON ===
with open('final_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# === Step 2: Turkish vowel-based course letters ===
course_letters = {"a", "e", "ı", "i", "o", "ö", "u", "ü"}

# === Step 3: Add 'courses' array to each word ===
for entry in data:
    word_text = entry["word"].lower()
    courses = sorted({letter for letter in word_text if letter in course_letters})
    entry["courses"] = courses

# === Step 4: Save new JSON with courses added ===
with open('final_output_with_courses.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ New JSON with courses saved as: final_output_with_courses.json")
