import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_nightlight():
    # Create directory for images if it doesn't exist
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
        
    if not os.path.exists('static/images/killers'):
        os.makedirs('static/images/killers')
        
    if not os.path.exists('static/images/survivors'):
        os.makedirs('static/images/survivors')
        
    if not os.path.exists('static/images/perks'):
        os.makedirs('static/images/perks')
    
    # Scrape killers
    killers_data = scrape_killers()
    
    # Scrape survivors
    survivors_data = scrape_survivors()
    
    # Scrape perks
    perks_data = scrape_perks()
    
    # Save all data to a JSON file for reference
    all_data = {
        'killers': killers_data,
        'survivors': survivors_data,
        'perks': perks_data
    }
    
    with open('scraped_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print("Scraping completed. Data saved to scraped_data.json")

def scrape_killers():
    print("Scraping killers...")
    killers_url = "https://nightlight.gg/killers"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    
    response = requests.get(killers_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to get killers. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    killer_cards = soup.select('.killer-card')
    
    killers = []
    for card in killer_cards:
        try:
            killer_link = card.find('a')['href']
            killer_id = killer_link.split('/')[-1]
            
            name_elem = card.select_one('.killer-card-name')
            name = name_elem.text.strip() if name_elem else "Unknown"
            
            # Get the image
            img_elem = card.select_one('img')
            if img_elem and 'src' in img_elem.attrs:
                img_url = img_elem['src']
                if img_url.startswith('/'):
                    img_url = f"https://nightlight.gg{img_url}"
                
                # Download the image
                img_response = requests.get(img_url, headers=headers)
                if img_response.status_code == 200:
                    with open(f'static/images/killers/{killer_id}.png', 'wb') as img_file:
                        img_file.write(img_response.content)
            
            # Scrape detailed information for each killer
            killer_detail = scrape_killer_detail(killer_id)
            
            killers.append({
                'id': killer_id,
                'name': name,
                'details': killer_detail
            })
            
            print(f"Scraped killer: {name}")
            
        except Exception as e:
            print(f"Error processing killer card: {e}")
    
    return killers

def scrape_killer_detail(killer_id):
    detail_url = f"https://nightlight.gg/killers/{killer_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    
    response = requests.get(detail_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to get killer detail for {killer_id}. Status code: {response.status_code}")
        return {}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        # Extract real name, difficulty, power, etc.
        real_name = ""
        power_name = ""
        power_description = ""
        
        info_sections = soup.select('.killer-info-section')
        for section in info_sections:
            title = section.select_one('.killer-info-title')
            if title:
                title_text = title.text.strip()
                content = section.select_one('.killer-info-content')
                
                if 'Real Name' in title_text and content:
                    real_name = content.text.strip()
                elif 'Power' in title_text and content:
                    power_texts = content.find_all('p')
                    if power_texts and len(power_texts) > 0:
                        power_name = power_texts[0].text.strip()
                        if len(power_texts) > 1:
                            power_description = power_texts[1].text.strip()
        
        # Extract overview, lore, etc.
        overview = ""
        lore = ""
        
        overview_section = soup.select_one('.killer-overview')
        if overview_section:
            overview = overview_section.text.strip()
        
        lore_section = soup.select_one('.killer-lore')
        if lore_section:
            lore = lore_section.text.strip()
        
        # Extract perks
        perks = []
        perk_elements = soup.select('.killer-perk')
        for perk_elem in perk_elements:
            perk_name_elem = perk_elem.select_one('.killer-perk-name')
            perk_desc_elem = perk_elem.select_one('.killer-perk-description')
            
            if perk_name_elem and perk_desc_elem:
                perk_name = perk_name_elem.text.strip()
                perk_desc = perk_desc_elem.text.strip()
                
                # Get perk image
                perk_img = perk_elem.select_one('img')
                if perk_img and 'src' in perk_img.attrs:
                    perk_img_url = perk_img['src']
                    if perk_img_url.startswith('/'):
                        perk_img_url = f"https://nightlight.gg{perk_img_url}"
                    
                    # Create a perk ID from the name
                    perk_id = perk_name.lower().replace(' ', '_').replace("'", '').replace('"', '')
                    
                    # Download the perk image
                    img_response = requests.get(perk_img_url)
                    if img_response.status_code == 200:
                        with open(f'static/images/perks/{perk_id}.png', 'wb') as img_file:
                            img_file.write(img_response.content)
                
                perks.append({
                    'name': perk_name,
                    'description': perk_desc
                })
        
        return {
            'real_name': real_name,
            'power': {
                'name': power_name,
                'description': power_description
            },
            'overview': overview,
            'lore': lore,
            'perks': perks
        }
        
    except Exception as e:
        print(f"Error processing killer detail for {killer_id}: {e}")
        return {}

def scrape_survivors():
    print("Scraping survivors...")
    survivors_url = "https://nightlight.gg/survivors"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    
    response = requests.get(survivors_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to get survivors. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    survivor_cards = soup.select('.survivor-card')
    
    survivors = []
    for card in survivor_cards:
        try:
            survivor_link = card.find('a')['href']
            survivor_id = survivor_link.split('/')[-1]
            
            name_elem = card.select_one('.survivor-card-name')
            name = name_elem.text.strip() if name_elem else "Unknown"
            
            # Get the image
            img_elem = card.select_one('img')
            if img_elem and 'src' in img_elem.attrs:
                img_url = img_elem['src']
                if img_url.startswith('/'):
                    img_url = f"https://nightlight.gg{img_url}"
                
                # Download the image
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    with open(f'static/images/survivors/{survivor_id}.png', 'wb') as img_file:
                        img_file.write(img_response.content)
            
            # Scrape detailed information for each survivor
            survivor_detail = scrape_survivor_detail(survivor_id)
            
            survivors.append({
                'id': survivor_id,
                'name': name,
                'details': survivor_detail
            })
            
            print(f"Scraped survivor: {name}")
            
        except Exception as e:
            print(f"Error processing survivor card: {e}")
    
    return survivors

def scrape_survivor_detail(survivor_id):
    detail_url = f"https://nightlight.gg/survivors/{survivor_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    
    response = requests.get(detail_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to get survivor detail for {survivor_id}. Status code: {response.status_code}")
        return {}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        # Extract description, backstory, etc.
        overview = ""
        lore = ""
        
        overview_section = soup.select_one('.survivor-overview')
        if overview_section:
            overview = overview_section.text.strip()
        
        lore_section = soup.select_one('.survivor-lore')
        if lore_section:
            lore = lore_section.text.strip()
        
        # Extract perks
        perks = []
        perk_elements = soup.select('.survivor-perk')
        for perk_elem in perk_elements:
            perk_name_elem = perk_elem.select_one('.survivor-perk-name')
            perk_desc_elem = perk_elem.select_one('.survivor-perk-description')
            
            if perk_name_elem and perk_desc_elem:
                perk_name = perk_name_elem.text.strip()
                perk_desc = perk_desc_elem.text.strip()
                
                # Get perk image
                perk_img = perk_elem.select_one('img')
                if perk_img and 'src' in perk_img.attrs:
                    perk_img_url = perk_img['src']
                    if perk_img_url.startswith('/'):
                        perk_img_url = f"https://nightlight.gg{perk_img_url}"
                    
                    # Create a perk ID from the name
                    perk_id = perk_name.lower().replace(' ', '_').replace("'", '').replace('"', '')
                    
                    # Download the perk image
                    img_response = requests.get(perk_img_url)
                    if img_response.status_code == 200:
                        with open(f'static/images/perks/{perk_id}.png', 'wb') as img_file:
                            img_file.write(img_response.content)
                
                perks.append({
                    'name': perk_name,
                    'description': perk_desc
                })
        
        return {
            'overview': overview,
            'lore': lore,
            'perks': perks
        }
        
    except Exception as e:
        print(f"Error processing survivor detail for {survivor_id}: {e}")
        return {}

def scrape_perks():
    print("Scraping perks...")
    perks_url = "https://nightlight.gg/perks"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    
    response = requests.get(perks_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to get perks. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    perk_elements = soup.select('.perk-card')
    
    perks = []
    for perk_elem in perk_elements:
        try:
            # Extract perk name and description
            perk_name_elem = perk_elem.select_one('.perk-name')
            perk_desc_elem = perk_elem.select_one('.perk-description')
            
            if perk_name_elem and perk_desc_elem:
                perk_name = perk_name_elem.text.strip()
                perk_desc = perk_desc_elem.text.strip()
                
                # Determine if it's a killer or survivor perk
                is_killer = False
                is_survivor = False
                
                if perk_elem.select_one('.killer-perk'):
                    is_killer = True
                elif perk_elem.select_one('.survivor-perk'):
                    is_survivor = True
                
                # Get perk image
                perk_img = perk_elem.select_one('img')
                if perk_img and 'src' in perk_img.attrs:
                    perk_img_url = perk_img['src']
                    if perk_img_url.startswith('/'):
                        perk_img_url = f"https://nightlight.gg{perk_img_url}"
                    
                    # Create a perk ID from the name
                    perk_id = perk_name.lower().replace(' ', '_').replace("'", '').replace('"', '')
                    
                    # Download the perk image
                    img_response = requests.get(perk_img_url)
                    if img_response.status_code == 200:
                        with open(f'static/images/perks/{perk_id}.png', 'wb') as img_file:
                            img_file.write(img_response.content)
                
                perks.append({
                    'name': perk_name,
                    'description': perk_desc,
                    'is_killer': is_killer,
                    'is_survivor': is_survivor
                })
                
                print(f"Scraped perk: {perk_name}")
                
        except Exception as e:
            print(f"Error processing perk card: {e}")
    
    return perks

if __name__ == "__main__":
    scrape_nightlight()