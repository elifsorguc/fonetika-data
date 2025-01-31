import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of RTÜK Telaffuz Sözlüğü page (for example purposes, this may need to be adapted)
BASE_URL = "https://www.radiotvregulation.org.tr/telaffuzsozlugu"  # Change with the actual base URL

# Directory to save audio files
AUDIO_DIR = "audio_files"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Headers to simulate a real user request (some websites might block non-browser requests)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Function to extract data for each word from its specific page
def extract_word_data(word_url):
    word_data = {}
    response = requests.get(word_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the word
    word = soup.find("div", class_="lh col-md-10 col-sm-10 col-xs-9").text.strip()

    # Extract phonetic transcription
    phonetic = soup.find("dd").find("div", class_="yazilis").text.strip()

    # Extract audio file URL
    audio_tag = soup.find("audio")
    audio_url = urljoin(BASE_URL, audio_tag["src"]) if audio_tag else None

    word_data['word'] = word
    word_data['phonetic'] = phonetic
    word_data['audio_url'] = audio_url

    return word_data

# Function to scrape the list of words from the search results page
def scrape_words(start_page=1, end_page=2):
    words_data = []
    for page_num in range(start_page, end_page + 1):
        print(f"Scraping page {page_num}")
        search_url = f"{BASE_URL}/search?page={page_num}"  # Adapt to actual search URL
        response = requests.get(search_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all word links (this is a placeholder, adapt it to your website's structure)
        word_links = soup.find_all("a", class_="search-link-class")  # Adapt with actual link class
        for link in word_links:
            word_url = urljoin(BASE_URL, link["href"])
            word_data = extract_word_data(word_url)
            words_data.append(word_data)
    
    return words_data

# Function to download audio files from the URLs
def download_audio(audio_url, word):
    if audio_url:
        audio_response = requests.get(audio_url, headers=HEADERS)
        audio_filename = os.path.join(AUDIO_DIR, f"{word}.mp3")  # Save as MP3
        with open(audio_filename, "wb") as audio_file:
            audio_file.write(audio_response.content)
        print(f"Downloaded audio for {word}")
        return audio_filename
    return None

# Create a DataFrame from the scraped data
def create_dataset():
    words_data = scrape_words(start_page=1, end_page=2)  # Adjust start and end page as needed
    dataset = []

    # Download audio files and build the dataset
    for word_data in words_data:
        word = word_data["word"]
        phonetic = word_data["phonetic"]
        audio_url = word_data["audio_url"]
        audio_filename = download_audio(audio_url, word)

        dataset.append({
            "word": word,
            "phonetic": phonetic,
            "audio_file": audio_filename
        })

    # Save dataset to a CSV file
    df = pd.DataFrame(dataset)
    df.to_csv("telaffuz_sozlugu_dataset.csv", index=False)
    print("Dataset saved to telaffuz_sozlugu_dataset.csv")

# Run the dataset creation process
create_dataset()
