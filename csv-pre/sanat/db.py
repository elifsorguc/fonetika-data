import json
from pymongo import MongoClient

# === Step 1: Load structured JSON file ===
with open('last.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# === Step 2: Connect to MongoDB Atlas ===
client = MongoClient("mongodb+srv://fonetika:a9Dppy2d.%40JFRRq@fonetika.28eco.mongodb.net/fonetika_db?retryWrites=true&w=majority")

# Your database & collection names
db = client['fonetika_db']             # Change if needed
collection = db['art_words']                   # Change if needed

# === Step 3: Insert All Words ===
result = collection.insert_many(data)

print(f"✅ Successfully inserted {len(result.inserted_ids)} words into MongoDB Atlas.")

