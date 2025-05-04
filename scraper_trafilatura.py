import trafilatura
import json
import os
import time
import re
from bs4 import BeautifulSoup

def scrape_nightlight():
    """Main scraping function"""
    # Create directory for images if it doesn't exist
    for dir_path in ['static/images/killers', 'static/images/survivors', 'static/images/perks']:
        os.makedirs(dir_path, exist_ok=True)
    
    # URLs to scrape
    killers_url = "https://nightlight.gg/killers"
    survivors_url = "https://nightlight.gg/survivors"
    perks_url = "https://nightlight.gg/perks"
    
    # Scrape killers
    print("Scraping killers...")
    killers_data = scrape_killers(killers_url)
    
    # Sleep to avoid rate limiting
    time.sleep(2)
    
    # Scrape survivors
    print("Scraping survivors...")
    survivors_data = scrape_survivors(survivors_url)
    
    # Sleep to avoid rate limiting
    time.sleep(2)
    
    # Scrape perks
    print("Scraping perks...")
    perks_data = scrape_perks(perks_url)
    
    # Save all data to a JSON file for reference
    all_data = {
        'killers': killers_data,
        'survivors': survivors_data,
        'perks': perks_data
    }
    
    with open('scraped_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print("Scraping completed. Data saved to scraped_data.json")

def download_with_trafilatura(url):
    """Download and extract content from a URL using trafilatura"""
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            content = trafilatura.extract(downloaded, output_format='xml', include_images=True, include_links=True)
            return content
        else:
            print(f"Failed to download content from {url}")
    except Exception as e:
        print(f"Error downloading content from {url}: {e}")
    return None

def extract_image_urls(xml_content):
    """Extract image URLs from XML content"""
    if not xml_content:
        return []
    
    # Parse XML content
    soup = BeautifulSoup(xml_content, 'xml')
    
    # Find all image tags
    image_tags = soup.find_all('graphic')
    
    # Extract URLs
    image_urls = []
    for img in image_tags:
        if 'url' in img.attrs:
            image_urls.append(img['url'])
    
    return image_urls

def extract_links(xml_content):
    """Extract links from XML content"""
    if not xml_content:
        return []
    
    # Parse XML content
    soup = BeautifulSoup(xml_content, 'xml')
    
    # Find all link tags
    link_tags = soup.find_all('ref')
    
    # Extract links
    links = []
    for link in link_tags:
        if 'target' in link.attrs:
            links.append({
                'url': link['target'],
                'text': link.text.strip()
            })
    
    return links

def scrape_killers(url):
    """Scrape killer data"""
    killers = []
    
    # Get the killers page
    xml_content = download_with_trafilatura(url)
    if not xml_content:
        return killers
    
    # Extract links to killer details
    links = extract_links(xml_content)
    
    # Filter links to killer details
    killer_links = [link for link in links if '/killers/' in link['url'] and not link['url'].endswith('/killers')]
    
    for link in killer_links:
        try:
            # Extract killer ID and name
            killer_url = link['url']
            killer_id = killer_url.split('/')[-1]
            killer_name = link['text']
            
            print(f"Found killer: {killer_name} (ID: {killer_id})")
            
            # Scrape killer details
            killer_detail = scrape_killer_detail(killer_url)
            
            killers.append({
                'id': killer_id,
                'name': killer_name,
                'details': killer_detail
            })
            
            # Sleep to avoid rate limiting
            time.sleep(1)
            
        except Exception as e:
            print(f"Error processing killer {link['text']}: {e}")
    
    return killers

def scrape_killer_detail(url):
    """Scrape details for a specific killer"""
    detail = {}
    
    # Get the killer detail page
    xml_content = download_with_trafilatura(url)
    if not xml_content:
        return detail
    
    # Process the content
    soup = BeautifulSoup(xml_content, 'xml')
    
    # Extract all text sections
    sections = soup.find_all('div')
    
    # Extract data
    overview = ""
    lore = ""
    real_name = ""
    power_name = ""
    power_description = ""
    
    for section in sections:
        section_text = section.text.strip()
        
        # Look for sections based on their content
        if "Overview" in section_text or "Background" in section_text:
            overview = section_text
        elif "Lore" in section_text or "Backstory" in section_text:
            lore = section_text
        elif "Real Name" in section_text:
            real_name = section_text.replace("Real Name:", "").strip()
        elif "Power:" in section_text:
            power_parts = section_text.split("\n", 1)
            if len(power_parts) > 0:
                power_name = power_parts[0].replace("Power:", "").strip()
            if len(power_parts) > 1:
                power_description = power_parts[1].strip()
    
    # Extract perks (look for sections that might contain perk information)
    perks = []
    possible_perk_sections = [s for s in sections if "perk" in s.text.lower()]
    
    for perk_section in possible_perk_sections:
        perk_text = perk_section.text.strip()
        
        # Try to extract perk name and description
        lines = perk_text.split("\n")
        if len(lines) >= 2:
            perk_name = lines[0].strip()
            perk_desc = "\n".join(lines[1:]).strip()
            
            perks.append({
                'name': perk_name,
                'description': perk_desc
            })
    
    # Extract image URLs for the killer
    image_urls = extract_image_urls(xml_content)
    
    # Save the first image as the killer portrait
    if image_urls and len(image_urls) > 0:
        try:
            # Save killer image locally
            save_image_from_url(image_urls[0], f"static/images/killers/{url.split('/')[-1]}.png")
        except Exception as e:
            print(f"Error saving killer image: {e}")
    
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

def scrape_survivors(url):
    """Scrape survivor data"""
    survivors = []
    
    # Get the survivors page
    xml_content = download_with_trafilatura(url)
    if not xml_content:
        return survivors
    
    # Extract links to survivor details
    links = extract_links(xml_content)
    
    # Filter links to survivor details
    survivor_links = [link for link in links if '/survivors/' in link['url'] and not link['url'].endswith('/survivors')]
    
    for link in survivor_links:
        try:
            # Extract survivor ID and name
            survivor_url = link['url']
            survivor_id = survivor_url.split('/')[-1]
            survivor_name = link['text']
            
            print(f"Found survivor: {survivor_name} (ID: {survivor_id})")
            
            # Scrape survivor details
            survivor_detail = scrape_survivor_detail(survivor_url)
            
            survivors.append({
                'id': survivor_id,
                'name': survivor_name,
                'details': survivor_detail
            })
            
            # Sleep to avoid rate limiting
            time.sleep(1)
            
        except Exception as e:
            print(f"Error processing survivor {link['text']}: {e}")
    
    return survivors

def scrape_survivor_detail(url):
    """Scrape details for a specific survivor"""
    detail = {}
    
    # Get the survivor detail page
    xml_content = download_with_trafilatura(url)
    if not xml_content:
        return detail
    
    # Process the content
    soup = BeautifulSoup(xml_content, 'xml')
    
    # Extract all text sections
    sections = soup.find_all('div')
    
    # Extract data
    overview = ""
    lore = ""
    
    for section in sections:
        section_text = section.text.strip()
        
        # Look for sections based on their content
        if "Overview" in section_text or "Background" in section_text:
            overview = section_text
        elif "Lore" in section_text or "Backstory" in section_text:
            lore = section_text
    
    # Extract perks (look for sections that might contain perk information)
    perks = []
    possible_perk_sections = [s for s in sections if "perk" in s.text.lower()]
    
    for perk_section in possible_perk_sections:
        perk_text = perk_section.text.strip()
        
        # Try to extract perk name and description
        lines = perk_text.split("\n")
        if len(lines) >= 2:
            perk_name = lines[0].strip()
            perk_desc = "\n".join(lines[1:]).strip()
            
            perks.append({
                'name': perk_name,
                'description': perk_desc
            })
    
    # Extract image URLs for the survivor
    image_urls = extract_image_urls(xml_content)
    
    # Save the first image as the survivor portrait
    if image_urls and len(image_urls) > 0:
        try:
            # Save survivor image locally
            save_image_from_url(image_urls[0], f"static/images/survivors/{url.split('/')[-1]}.png")
        except Exception as e:
            print(f"Error saving survivor image: {e}")
    
    return {
        'overview': overview,
        'lore': lore,
        'perks': perks
    }

def scrape_perks(url):
    """Scrape all perks from the perks page"""
    perks = []
    
    # Get the perks page
    xml_content = download_with_trafilatura(url)
    if not xml_content:
        return perks
    
    # Process the content
    soup = BeautifulSoup(xml_content, 'xml')
    
    # Extract all text sections
    sections = soup.find_all('div')
    
    # Look for perk sections
    for section in sections:
        section_text = section.text.strip()
        
        if "perk" in section_text.lower():
            try:
                # Try to extract perk name and description
                lines = section_text.split("\n")
                if len(lines) >= 2:
                    perk_name = lines[0].strip()
                    perk_desc = "\n".join(lines[1:]).strip()
                    
                    # Determine if it's a killer or survivor perk
                    is_killer = "killer" in section_text.lower()
                    is_survivor = "survivor" in section_text.lower()
                    
                    perks.append({
                        'name': perk_name,
                        'description': perk_desc,
                        'is_killer': is_killer,
                        'is_survivor': is_survivor
                    })
                    
                    print(f"Scraped perk: {perk_name}")
            except Exception as e:
                print(f"Error processing perk section: {e}")
    
    return perks

def save_image_from_url(url, save_path):
    """Download an image from a URL and save it locally"""
    import requests
    
    try:
        # Set headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as img_file:
                img_file.write(response.content)
            print(f"Saved image to {save_path}")
            return True
        else:
            print(f"Failed to download image from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error saving image from {url}: {e}")
    
    return False

if __name__ == "__main__":
    scrape_nightlight()