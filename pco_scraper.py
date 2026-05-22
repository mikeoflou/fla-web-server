import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

load_dotenv()

def get_pco_data():
    """
    Scrape PCO Services to get order of worship data.
    Returns dict with song_ids and song_titles lists.
    """
    email = os.getenv('PCO_EMAIL')
    password = os.getenv('PCO_PASSWORD')
    
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run without GUI
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Navigate to PCO login page
        driver.get('https://accounts.planningcenteronline.com/sign_in')
        
        # Wait for email field and enter credentials
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'user[email_address]'))
        )
        email_field.send_keys(email)
        
        password_field = driver.find_element(By.NAME, 'user[password]')
        password_field.send_keys(password)
        
        # Click login button
        login_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_btn.click()
        
        # Wait for redirect to services page
        time.sleep(3)
        driver.get('https://services.planningcenteronline.com/matrix/reloaded')
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'song'))
        )
        
        # Extract song data
        song_elements = driver.find_elements(By.CLASS_NAME, 'song')
        
        song_ids = []
        song_titles = []
        
        for song in song_elements:
            try:
                # Extract title
                title_elem = song.find_element(By.CLASS_NAME, 'title')
                title = title_elem.text.strip()
                
                # Extract YouTube ID from data attribute or link
                # PCO might store it in different ways, adjust as needed
                youtube_id = song.get_attribute('data-youtube-id')
                if not youtube_id:
                    # Try to extract from link
                    link = song.find_element(By.TAG_NAME, 'a')
                    href = link.get_attribute('href')
                    # Extract YouTube ID from URL if present
                    if 'youtube.com/watch?v=' in href:
                        youtube_id = href.split('v=')[1].split('&')[0]
                    elif 'youtu.be/' in href:
                        youtube_id = href.split('youtu.be/')[1]
                
                if title and youtube_id:
                    song_titles.append(title)
                    song_ids.append(youtube_id)
            except:
                continue
        
        return {
            'song_ids': song_ids,
            'song_titles': song_titles
        }
    
    except Exception as e:
        print(f"Error scraping PCO: {e}")
        return {
            'song_ids': [],
            'song_titles': []
        }
    
    finally:
        driver.quit()


if __name__ == '__main__':
    data = get_pco_data()
    print("Song IDs:", data['song_ids'])
    print("Song Titles:", data['song_titles'])
