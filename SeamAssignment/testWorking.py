import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Google search query (using a User-Agent to simulate a browser)
query = 'Elon Musk Latest Podcast'
url = f'https://www.google.com/search?q={query}'

# Updated headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
}

# Send a request to Google
response = requests.get(url, headers=headers)

# Check the status code
if response.status_code == 200:
    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the video section - inspect the page for the specific tags and classes
    video_section = soup.find_all('div', {'class': 'g'})  # Adjust this as needed

    search_list = []

    # Iterate through the first few rows (change limit as needed)
    for idx, video in enumerate(video_section[:10]):  # Limit to the first 3 video results
        title = video.find('h3').text if video.find('h3') else 'No title'
        link = video.find('a')['href'] if video.find('a') else 'No link'
        print(f'\n{idx + 1}: {title} - {link}')
        search_list.append({'title': title, 'link': link})

    # To store the latest video
    latest_video = None

    # Inside the loop that processes each video link
    for item in search_list:
        video_url = item['link']
        
        # Send a request to the YouTube video page
        video_response = requests.get(video_url, headers=headers)
        
        if video_response.status_code == 200:
            # Parse the video page content
            video_soup = BeautifulSoup(video_response.text, 'html.parser')

            # Find the publish date (this part depends on the YouTube page structure)
            date_element = video_soup.find('meta', {'itemprop': 'datePublished'})
            if date_element:
                publish_date = date_element['content']
                # Adjust format to handle full ISO 8601 date-time
                formatted_date = datetime.fromisoformat(publish_date.replace("Z", "+00:00"))
                
                # Check if this video is the latest
                if latest_video is None or formatted_date > latest_video['date']:
                    latest_video = {
                        'title': item['title'],
                        'link': video_url,
                        'date': formatted_date
                    }
            else:
                print(f"No publish date found for: {item['title']}")
        else:
            print(f"Failed to retrieve video page: {video_url} with status code: {video_response.status_code}")

    # Output the latest video information
    if latest_video:
        print(f"\nLatest Video:\nTitle: {latest_video['title']}\nLink: {latest_video['link']}\nPublished: {latest_video['date']}")
    else:
        print("No videos with a publish date found.")
else:
    print(f"Request failed with status code: {response.status_code}")
