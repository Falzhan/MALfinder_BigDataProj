import requests
from bs4 import BeautifulSoup

def get_anime_cover(mal_url):
    """
    Scrapes the MyAnimeList page to find the cover image.
    Looks for <img itemprop="image"> and prefers data-src over src.
    """
    if not mal_url:
        return None
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(mal_url, headers=headers, timeout=3)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Target the specific image tag structure provided
            # <img ... itemprop="image" ...>
            img_tag = soup.find('img', {'itemprop': 'image'})
            
            if img_tag:
                # MAL often uses lazy loading, so the real image is in data-src
                if img_tag.get('data-src'):
                    return img_tag.get('data-src')
                elif img_tag.get('src'):
                    return img_tag.get('src')
                    
    except Exception as e:
        print(f"Error scraping image for {mal_url}: {e}")
        return None
    
    return None