import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re

load_dotenv()

def get_pco_songs():
    """
    Scrape PCO Services using BeautifulSoup to extract song titles and YouTube IDs.
    Returns list of dicts with 'title' and 'youtube_id'.
    """
    email = os.getenv('PCO_EMAIL')
    password = os.getenv('PCO_PASSWORD')
    
    try:
        # Create session to handle cookies and maintain login
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Step 1: Login to Planning Center
        login_url = 'https://accounts.planningcenteronline.com/sign_in'
        
        # Get CSRF token from login page
        login_page = session.get(login_url)
        soup = BeautifulSoup(login_page.content, 'html.parser')
        
        # Find csrf token
        csrf_token = None
        for input_tag in soup.find_all('input'):
            if input_tag.get('name') == 'authenticity_token':
                csrf_token = input_tag.get('value')
                break
        
        # Login
        login_data = {
            'user[email_address]': email,
            'user[password]': password,
            'authenticity_token': csrf_token or '',
            'commit': 'Sign In'
        }
        
        response = session.post(login_url, data=login_data)
        
        # Step 2: Navigate to Services/Matrix page
        services_url = 'https://services.planningcenteronline.com/matrix/reloaded'
        services_page = session.get(services_url)
        
        if services_page.status_code != 200:
            print(f"Failed to access services: {services_page.status_code}")
            return []
        
        # Step 3: Parse HTML to find songs
        soup = BeautifulSoup(services_page.content, 'html.parser')
        songs = []
        
        # Look for song elements (adjust selector based on PCO HTML structure)
        # Try different potential selectors
        song_elements = soup.find_all(class_=re.compile(r'song|plan-item|thumbnail'))
        
        for element in song_elements:
            try:
                # Extract title
                title = None
                title_elem = element.find(class_=re.compile(r'title|name'))
                if title_elem:
                    title = title_elem.get_text(strip=True)
                
                # Extract YouTube ID from data attribute or link
                youtube_id = None
                
                # Try data attribute
                youtube_id = element.get('data-youtube-id')
                
                # Try finding a link with YouTube URL
                if not youtube_id:
                    for link in element.find_all('a'):
                        href = link.get('href', '')
                        if 'youtube.com' in href or 'youtu.be' in href:
                            if 'youtube.com/watch?v=' in href:
                                youtube_id = href.split('v=')[1].split('&')[0]
                            elif 'youtu.be/' in href:
                                youtube_id = href.split('youtu.be/')[1].split('?')[0]
                            break
                
                # Try finding YouTube ID in text or attributes
                if not youtube_id:
                    for key in element.attrs:
                        if isinstance(element.attrs[key], str):
                            # Check if YouTube ID pattern exists
                            youtube_match = re.search(r'[a-zA-Z0-9_-]{11}', element.attrs[key])
                            if youtube_match:
                                youtube_id = youtube_match.group()
                                break
                
                if title and youtube_id:
                    songs.append({
                        'title': title,
                        'youtube_id': youtube_id
                    })
            except Exception as e:
                print(f"Error parsing song element: {e}")
                continue
        
        return songs
    
    except Exception as e:
        print(f"Error scraping PCO: {e}")
        import traceback
        traceback.print_exc()
        return []


if __name__ == '__main__':
    songs = get_pco_songs()
    print(f"Found {len(songs)} songs:")
    for song in songs:
        print(f"  - {song['title']} ({song['youtube_id']})")
