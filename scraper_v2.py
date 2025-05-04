import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re

def get_headers():
    """Return headers to mimic a browser request"""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }

def download_image(url, save_path):
    """Download an image and save it to the specified path"""
    headers = get_headers()
    try:
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as img_file:
                for chunk in response.iter_content(chunk_size=8192):
                    img_file.write(chunk)
            print(f"Downloaded image: {os.path.basename(save_path)}")
            return True
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
    return False

def make_request(url):
    """Make a request to a URL and return the BeautifulSoup object"""
    headers = get_headers()
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"Failed to get {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error making request to {url}: {e}")
    return None

def clean_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def save_image(url, folder, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            os.makedirs(folder, exist_ok=True)
            clean_name = clean_filename(filename)
            with open(f"{folder}/{clean_name}.png", 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Error saving image {filename}: {e}")
    return False

def scrape_dbd_wiki():
    base_url = "https://deadbydaylight.fandom.com"

    # Scrape killers
    killers_url = f"{base_url}/wiki/Killers"
    survivors_url = f"{base_url}/wiki/Survivors"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    data = {"killers": [], "survivors": []}

    # Scrape Killers
    print("Scraping killers...")
    response = requests.get(killers_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        killer_tables = soup.find_all('table', class_='wikitable')

        for table in killer_tables:
            rows = table.find_all('tr')[1:]  # Skip header
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    try:
                        image_cell = cells[0]
                        img_tag = image_cell.find('img')
                        if img_tag and 'data-src' in img_tag.attrs:
                            image_url = img_tag['data-src']
                            if '?' in image_url:
                                image_url = image_url.split('?')[0]

                            name_cell = cells[1]
                            killer_name = name_cell.get_text(strip=True)

                            save_image(image_url, "static/images/killers", killer_name)
                            print(f"Saved killer image: {killer_name}")
                            time.sleep(1)  # Be nice to the server
                    except Exception as e:
                        print(f"Error processing killer: {e}")

    # Scrape Survivors
    print("\nScraping survivors...")
    response = requests.get(survivors_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        survivor_tables = soup.find_all('table', class_='wikitable')

        for table in survivor_tables:
            rows = table.find_all('tr')[1:]  # Skip header
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    try:
                        image_cell = cells[0]
                        img_tag = image_cell.find('img')
                        if img_tag and 'data-src' in img_tag.attrs:
                            image_url = img_tag['data-src']
                            if '?' in image_url:
                                image_url = image_url.split('?')[0]

                            name_cell = cells[1]
                            survivor_name = name_cell.get_text(strip=True)

                            save_image(image_url, "static/images/survivors", survivor_name)
                            print(f"Saved survivor image: {survivor_name}")
                            time.sleep(1)  # Be nice to the server
                    except Exception as e:
                        print(f"Error processing survivor: {e}")

    return data

if __name__ == "__main__":
    scrape_dbd_wiki()