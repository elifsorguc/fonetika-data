import os
import csv
import requests
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Create output folder
output_folder = "corpus"
os.makedirs(output_folder, exist_ok=True)

# Read dataset.csv and extract words with audio URLs
dataset_file = "dataset.csv"

# Function to download and convert an audio file
def process_audio(row):
    word, _, url, seskelime_number = row  # Extract word, ignore phonetic, use URL and ID

    if not word.strip() or not url.strip():  # Skip rows with missing word or URL
        return

    audio_filename = f"{seskelime_number}.wav"
    audio_path = os.path.join(output_folder, audio_filename)

    # Download the audio file
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        temp_mp3 = os.path.join(output_folder, f"{seskelime_number}.mp3")

        with open(temp_mp3, "wb") as f:
            f.write(response.content)

        # Convert to 16kHz Mono WAV using FFmpeg
        subprocess.run([
            "ffmpeg", "-y", "-i", temp_mp3, 
            "-ac", "1", "-ar", "16000", 
            audio_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        os.remove(temp_mp3)  # Remove temporary MP3 file
        print(f"✅ Processed: {audio_filename}")

    except requests.RequestException as e:
        print(f"❌ Failed to download {url}: {e}")

# Read CSV and start multithreading for faster downloads
with open(dataset_file, "r", encoding="utf-8") as infile:
    reader = csv.reader(infile)
    next(reader)  # Skip header

    valid_rows = [row for row in reader if row[0].strip() and row[2].strip()]  # Ensure word + URL exist

# Use multithreading to process multiple files at once (adjust max_workers as needed)
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(process_audio, valid_rows)

print("✅ All audio files are downloaded and converted!")
