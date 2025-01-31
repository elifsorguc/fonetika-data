import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# Base URL for RTÜK Telaffuz Sözlüğü
BASE_URL = "https://sozluk.rtuk.gov.tr"

# Directory to save audio files
AUDIO_DIR = "audio_files"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Headers to simulate a real user request (avoid blocking)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Function to search for the word and get the link to its page
def search_word(word):
    search_url = f"{BASE_URL}/Home/SozlukSorgula"
    params = {'searchtext': word}
    response = requests.get(search_url, headers=HEADERS, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    # Look for the first result (assuming it’s the correct word)
    word_links = soup.find_all("a", {"class": "search-link-class"})  # Adjust with the actual class
    if word_links:
        word_url = urljoin(BASE_URL, word_links[0]["href"])
        return word_url
    return None

# Function to scrape phonetic transcription and audio URL from the word's page
def extract_word_data(word_url):
    response = requests.get(word_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract phonetic transcription (e.g., under <dd>)
    phonetic_tag = soup.find("dd")  # Adjust with the correct tag based on your page
    phonetic = phonetic_tag.text.strip() if phonetic_tag else None

    # Extract the audio URL from the <audio> tag (src attribute)
    audio_tag = soup.find("audio")
    audio_url = urljoin(BASE_URL, audio_tag["src"]) if audio_tag else None

    return phonetic, audio_url

# Function to download the audio file
def download_audio(audio_url, word):
    if audio_url:
        audio_response = requests.get(audio_url, headers=HEADERS)
        audio_filename = os.path.join(AUDIO_DIR, f"{word}.mp3")  # Save as MP3
        with open(audio_filename, "wb") as audio_file:
            audio_file.write(audio_response.content)
        print(f"Downloaded audio for {word}")
        return audio_filename
    return None

# Main function to scrape for each word
def scrape_for_word(word):
    word_url = search_word(word)
    if word_url:
        print(f"Found word page for '{word}': {word_url}")
        phonetic, audio_url = extract_word_data(word_url)
        if phonetic and audio_url:
            print(f"Phonetic transcription for '{word}': {phonetic}")
            audio_filename = download_audio(audio_url, word)
            return phonetic, audio_filename
        else:
            print(f"Failed to extract phonetic transcription or audio for '{word}'")
    else:
        print(f"Word '{word}' not found in the search results.")
    return None, None

# Function to process words from CSV and scrape data
def process_words_from_csv(input_csv, output_csv):
    # Load words from CSV file
    df = pd.read_csv(input_csv)
    words = df['word'].tolist()  # Extract words into a list

    # Prepare a list to store the data
    dataset = []

    # Scrape data for each word
    for word in words:
        phonetic, audio_file = scrape_for_word(word)
        if phonetic and audio_file:
            dataset.append({
                "word": word,
                "phonetic": phonetic,
                "audio_file": audio_file
            })

    # Save the dataset to a new CSV file
    output_df = pd.DataFrame(dataset)
    output_df.to_csv(output_csv, index=False)
    print(f"Dataset saved to {output_csv}")

# Example usage
input_csv = "words.csv"  # Your input CSV file with words
output_csv = "scraped_words_dataset.csv"  # Output CSV file to save the scraped data

process_words_from_csv(input_csv, output_csv)
