import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import time
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

# Function to search for the word and get the link to its detailed page
def search_word(word):
    search_url = f"{BASE_URL}/Home/SozlukSorgula"
    params = {'searchtext': word}
    response = requests.get(search_url, headers=HEADERS, params=params)
    
    # Add delay to avoid rate-limiting or blocking
    time.sleep(1)  # Delay for 1 second between requests
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the first word link (this will contain the ID for the word)
    word_links = soup.find_all("a", {"class": "search-link-class"})  # Adjust with the actual class if needed
    
    if word_links:
        word_url = urljoin(BASE_URL, word_links[0]["href"])
        
        # Extract the ID from the word URL
        word_id = word_url.split('/')[-1]  # The ID is in the last part of the URL (e.g., SesKelime/9345)
        return word_id
    return None

# Function to scrape the phonetic transcription using the word ID
def extract_word_data(word_id):
    # Construct the URL for the word's audio
    audio_url = f"{BASE_URL}/Home/SesKelime/{word_id}"
    
    # Here, we might want to scrape the phonetic transcription if it's available on the same page
    phonetic_url = f"{BASE_URL}/Home/SozlukSorgula/{word_id}"  # Adjust if needed
    response = requests.get(phonetic_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Scrape phonetic transcription (adjust based on the website structure)
    phonetic_tag = soup.find("dd")  # Update if needed
    phonetic = phonetic_tag.text.strip() if phonetic_tag else "N/A"
    
    return phonetic, audio_url

# Function to download the audio file
def download_audio(audio_url, word):
    audio_response = requests.get(audio_url, headers=HEADERS)
    audio_filename = os.path.join(AUDIO_DIR, f"{word}.mp3")  # Save as MP3
    
    with open(audio_filename, "wb") as audio_file:
        audio_file.write(audio_response.content)
    
    print(f"Downloaded audio for {word}")
    return audio_filename

# Function to process words from the cleaned text file and scrape data
def process_words_from_txt(input_txt, output_csv):
    # Read the words from the cleaned txt file
    with open(input_txt, 'r', encoding='utf-8') as file:
        words = file.readlines()

    # Prepare a list to store the data
    dataset = []

    # Scrape data for each word
    for word in words:
        word = word.strip()  # Remove any extra spaces or newlines
        if word:  # Only scrape if the word is not empty
            word_id = search_word(word)  # Get the word ID
            if word_id:
                phonetic, audio_file = extract_word_data(word_id)
                if phonetic and audio_file:
                    dataset.append({
                        "word": word,
                        "phonetic": phonetic,
                        "audio_file": audio_file
                    })
            else:
                print(f"Skipping invalid word '{word}'")

    # Save the dataset to a new CSV file (only valid words)
    output_df = pd.DataFrame(dataset)
    output_df.to_csv(output_csv, index=False)
    print(f"Dataset saved to {output_csv}")

# Example usage
input_txt = 'cleaned_words.txt'  # The cleaned txt file with the words
output_csv = 'scraped_words_dataset.csv'  # Output CSV file to save the scraped data

# Call the function to process and scrape words
process_words_from_txt(input_txt, output_csv)
