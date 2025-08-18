import re
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Videoların idleri yputube tarafından başka sitelerde gösterilmemesi için buglı veya direkt engelli olabiliyor o durum düzeltilebilir.

class MetacriticScraper:
    SEARCH_URL = "https://www.metacritic.com/game"

    HEADERS = {
        "User-Agent": (
            "Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') 
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        self.driver = webdriver.Chrome(options=options)
    
    def search_game(self, game_title):
        try:
            title_slug = self.create_slug(game_title)
            search_url = f"https://www.metacritic.com/game/{title_slug}"
            
            print(f"🔍 Searched: {game_title}")
            print(f"🌐 URL: {search_url}")
            
            self.driver.get(search_url)
            

            try:
                read_more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.c-productDetails_readMore"))
                )
                self.driver.execute_script("arguments[0].click();", read_more_button)
                print("Pressed read more button")
                time.sleep(10)  
            except (TimeoutException, NoSuchElementException):
                print("There is no read more button")
            
           
            title_element = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="hero-title"] h1')
            score_element = self.driver.find_element(By.CSS_SELECTOR, '.c-siteReviewScore_background-critic_medium span[data-v-e408cafe]')
            
            try:
                description_element = self.driver.find_element(By.CSS_SELECTOR, 'span.c-productionDetailsGame_description.g-text-xsmall')
                game_description = description_element.text.strip()
                print(f"📝 Tam description alındı: {len(game_description)} karakter")
                print(f"📝 İçerik: {game_description[:200]}...")
            except NoSuchElementException:
                game_description = None
                print("📝 Description bulunamadı")
            
            if title_element and score_element:
                game_score = score_element.text.strip()
                
                return {
                    'title': game_title,
                    'score': int(game_score) if game_score.isdigit() else None,
                    'url': search_url,
                    'description': game_description,
                }
            
            return None
            
        except Exception as e:
            print(f"🚨 Hata: {e}")
            return None
        finally:
            self.driver.quit()
    

    def create_slug(self, title):
        """Oyun adını Metacritic slug formatına çevir"""
        # Küçük harfe çevir
        slug = title.lower()
        # Özel karakterleri kaldır
        slug = re.sub(r'[^\w\s-]', '', slug)
        # Boşlukları tire ile değiştir
        slug = re.sub(r'[-\s]+', '-', slug)
        # Baştan ve sondan tireleri temizle
        slug = slug.strip('-')
        return slug


class GameSpotScrapper():
    SEARCH_URL = "https://www.gamespot.com/games/"

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    } 

    def search_game(self,game_title):


        try:
            title_slug = self.create_slug(game_title)

            url = f"{self.SEARCH_URL}{title_slug}/"
            print(f"🔍 GameSpot'ta platform aranıyor: {game_title}")
            print(f"🌐 URL: {url}")


            response= requests.get(url,headers=self.HEADERS ,timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content,"html.parser")

            platforms = []

            platform_list = soup.find('ul',class_='system-list')

            if platform_list:
                platform_items = platform_list.find_all('li',class_=lambda x:x and 'system' in x)

                for item in platform_items:
                    platform_span = item.find('span' , itemprop="device")
                    if platform_span:
                        platform_name = platform_span.text.strip()
                        platforms.append(platform_name)
                print(f"Platform name added")
                return{
                    'platforms' : platforms,
                    'url': url,
                }
            else:
                print("There is no platform name")
                return None
        except requests.exceptions.RequestException as e:
            print(f"🚨 HTTP Hatası: {e}")
            return None
        except Exception as e:
            print(f"🚨 Genel Hata: {e}")
            return None
        
    def create_slug(self, title):
        """Oyun adını Metacritic slug formatına çevir"""
        # Küçük harfe çevir
        slug = title.lower()
        # Özel karakterleri kaldır
        slug = re.sub(r'[^\w\s-]', '', slug)
        # Boşlukları tire ile değiştir
        slug = re.sub(r'[-\s]+', '-', slug)
        # Baştan ve sondan tireleri temizle
        slug = slug.strip('-')
        return slug





    