import requests
import pandas as pd
from bs4 import BeautifulSoup
import concurrent.futures
import time

# Base URL for RTÜK Telaffuz Sözlüğü
BASE_URL = "https://sozluk.rtuk.gov.tr"

# Headers to simulate a real browser
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/91.0.4472.124 Safari/537.36'
    )
}

# Create a session for persistent cookies and headers
session = requests.Session()
session.headers.update(HEADERS)

def get_verification_token():
    """
    Retrieve the __RequestVerificationToken from the homepage.
    """
    response = session.get(BASE_URL)
    if response.status_code != 200:
        print("Error fetching homepage.")
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    token_input = soup.find("input", {"name": "__RequestVerificationToken"})
    if token_input:
        return token_input["value"]
    return None

def search_word(word):
    """
    Use the AJAX endpoint to search for the word and return the first result's ID.
    """
    search_url = f"{BASE_URL}/Home/SozlukSorgula"
    params = {'searchtext': word}
    try:
        response = session.get(search_url, params=params)
        # You can reduce or remove the delay for faster execution.
        # time.sleep(0.5)  
        data = response.json()  # JSON response
        if data:
            word_id = data[0]['Id']
            print(f"Found word '{word}' with ID: {word_id}")
            return word_id
    except Exception as e:
        print(f"Error searching for word '{word}': {e}")
    return None

def get_word_page(word, token, word_id):
    """
    Simulate the search form submission to retrieve the full HTML page (like View Source).
    """
    url = BASE_URL  # The form posts to the homepage
    form_data = {
        '__RequestVerificationToken': token,
        'SearchText': word,
        'SearchId': word_id
    }
    try:
        response = session.post(url, data=form_data)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: Received status {response.status_code} for word '{word}'")
    except Exception as e:
        print(f"Error fetching word page for '{word}': {e}")
    return None

def parse_word_page(html):
    """
    Parse the HTML page to extract the phonetic text and the original audio URL.
    """
    soup = BeautifulSoup(html, "html.parser")
    
    # Locate the phonetic transcription (Fonetik Yazım)
    phonetic = "N/A"
    dt_tag = soup.find("dt", string=lambda t: t and "Fonetik Yazım" in t)
    if dt_tag:
        dd_tag = dt_tag.find_next_sibling("dd")
        if dd_tag:
            phonetic = dd_tag.get_text(strip=True)
    
    # Locate the audio element and extract its src attribute (original URL)
    audio_url = None
    audio_tag = soup.find("audio", {"id": "player"})
    if audio_tag and audio_tag.get("src"):
        audio_url = requests.compat.urljoin(BASE_URL, audio_tag["src"])
    
    return phonetic, audio_url

def process_single_word(word, token):
    """
    Process a single word: search for it, get the full HTML page, and extract the phonetic text and audio URL.
    Returns a dictionary containing the word data or None if processing failed.
    """
    print(f"Processing word: '{word}'")
    word_id = search_word(word)
    if not word_id:
        print(f"Skipping '{word}' (no ID found)")
        return None

    html = get_word_page(word, token, word_id)
    if not html:
        print(f"Skipping '{word}' (could not retrieve page)")
        return None

    phonetic, audio_url = parse_word_page(html)
    print(f"Word: '{word}', Phonetic: '{phonetic}', Audio URL: '{audio_url}'")
    return {
        "word": word,
        "phonetic": phonetic,
        "audio_file": audio_url  # Keeping the original audio URL in the CSV
    }

def process_words_from_txt(input_txt, output_csv, max_workers=10):
    """
    For each word in the input text file, process concurrently to extract the phonetic text and the original audio URL.
    The results are saved to a CSV file.
    """
    token = get_verification_token()
    if not token:
        print("Unable to retrieve __RequestVerificationToken. Exiting.")
        return

    # Read words from the text file
    with open(input_txt, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]

    dataset = []

    # Use ThreadPoolExecutor to process multiple words concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks and collect futures
        futures = {executor.submit(process_single_word, word, token): word for word in words}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                dataset.append(result)
            # If you want a tiny delay between processing results, uncomment the following line:
            # time.sleep(0.1)

    # Save the collected data to CSV
    df = pd.DataFrame(dataset)
    df.to_csv(output_csv, index=False)
    print(f"\nDataset saved to '{output_csv}'")

# Example usage:
if __name__ == "__main__":
    input_txt = "cleaned_words.txt"       # Text file with one word per line
    output_csv = "scraped_words_dataset.csv"
    process_words_from_txt(input_txt, output_csv, max_workers=10)
