import requests
from bs4 import BeautifulSoup
import re

# Function to search Google for podcasts featuring the person
def search_podcast_on_web(person_name):
    search_query = f"{person_name} podcast"
    search_url = f"https://www.google.com/search?q={search_query}"
    
    headers = {
        "User-Agent": "Chrome/58.0.3029.110"
    }
    
    response = requests.get(search_url, headers=None)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all search result links
        links = soup.find_all('a', href=True)
        
        podcast_links = []
        
        for link in links:
            href = link['href']
            # Filter for podcast-related results (this regex looks for URLs that likely link to podcasts)
            if re.search(r'(youtube|latest?)', href):
                podcast_links.append(href)
        
        return podcast_links
    else:
        print("Failed to retrieve search results")
        return None

# Function to get podcast metadata and verify person
def verify_podcast(podcast_url, person_name):
    # Check if the podcast URL has a scheme (e.g., http or https)
    if not podcast_url.startswith('http'):
        podcast_url = "https://www.google.com" + podcast_url

    response = requests.get(podcast_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get the podcast episode title or description
        description = soup.find('meta', {'name': 'description'}) or soup.find('meta', {'property': 'og:description'})
        if description:
            description_text = description['content']
            
            # Verify if the person is mentioned
            if person_name.lower() in description_text.lower():
                return True
        
    return False

# Function to transcribe podcast using the Groq API (or similar)
def transcribe_podcast(podcast_url):
    # This is a pseudo-code for sending the podcast audio to a transcription service like Groq
    
    # Example flow:
    # - Download audio from the podcast URL
    # - Submit it to Groq API
    # - Get transcription response
    audio_file = download_podcast_audio(podcast_url)
    
    transcription_url = "https://api.groq.com/transcribe"
    headers = {
        "Authorization": "Bearer YOUR_GROQ_API_TOKEN",  # Replace with actual token
        "Content-Type": "application/json"
    }
    data = {
        "audio_file": audio_file  # Path to the downloaded podcast file
    }
    
    response = requests.post(transcription_url, headers=headers, json=data)
    
    if response.status_code == 200:
        transcription = response.json()['transcription']
        return transcription
    else:
        return "Transcription failed"

# Helper function to download podcast audio
def download_podcast_audio(podcast_url):
    # This function should download the podcast audio from the provided URL
    # For now, returning a mock path
    return "path_to_downloaded_audio.mp3"

# Main function to tie everything together
def get_latest_podcast_transcription(person_name):
    # Step 1: Search for the latest podcast featuring the person
    podcast_links = search_podcast_on_web(person_name)
    
    if not podcast_links:
        print(f"No podcast found for {person_name}")
        return
    
    # Step 2: Verify the podcast features the person and get the latest one
    for podcast_link in podcast_links:
        if verify_podcast(podcast_link, person_name):
            print(f"Found podcast: https:google.com{podcast_link}")
            
            # Step 3: Transcribe the podcast
            #transcription = transcribe_podcast(podcast_link)
            #print("Transcription:")
            #print(transcription)
            
            # Optionally save transcription to file
            #with open(f"{person_name}_podcast_transcription.txt", "w") as file:
            #   file.write(transcription)
            return
        else:
            print(f"{person_name} not mentioned in this podcast: https:google.com{podcast_link}")

# Example usage
get_latest_podcast_transcription("Elon Musk")
