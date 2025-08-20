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


class MetacriticScraper:
    SEARCH_URL = "https://www.metacritic.com/game"

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')          # Run Chrome in headless mode
        options.add_argument('--no-sandbox')            # Bypass OS security model
        options.add_argument('--disable-dev-shm-usage') # Overcome limited resource problems
        options.add_argument('--window-size=1920,1080') # Set fixed window size
        options.add_argument('--disable-blink-features=AutomationControlled') # Reduce bot detection
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        self.driver = webdriver.Chrome(options=options)

    def close(self):
        """Close the Selenium WebDriver properly."""
        try:
            self.driver.quit()
        except Exception:
            pass

    def search_game(self, game_title):
        """Search for a game on Metacritic and scrape its score and description."""
        try:
            # Convert game title into a slug for the URL
            title_slug = self.create_slug(game_title)
            search_url = f"https://www.metacritic.com/game/{title_slug}"
            print(f" Searched: {game_title}")
            print(f" URL: {search_url}")

            # Open the game page
            self.driver.get(search_url)

            # Wait until title element is present
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="hero-title"] h1'))
            )

            # Try clicking the "Read More" button if it exists
            try:
                read_more_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.c-productDetails_readMore"))
                )
                self.driver.execute_script("arguments[0].click();", read_more_button)
                print("Pressed read more button")
                time.sleep(1.0)
            except (TimeoutException, NoSuchElementException):
                print("There is no read more button")

            # Get the title element
            title_element = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="hero-title"] h1')

            # Try to find the score element (different selectors may appear)
            score_text = None
            for sel in [
                '.c-siteReviewScore_background-critic_medium span[data-v-e408cafe]',
                '[data-testid="metascore"]']:

                try:
                    score_element = self.driver.find_element(By.CSS_SELECTOR, sel)
                    score_text = score_element.text.strip()
                    if score_text:
                        break
                except NoSuchElementException:
                    continue

            # Try to extract the description
            try:
                description_element = self.driver.find_element(
                    By.CSS_SELECTOR, 'span.c-productionDetailsGame_description.g-text-xsmall'
                )
                game_description = description_element.text.strip()
                print(f" All description: {len(game_description)} characters")
                print(f"Short Description: {game_description[:200]}...")
            except NoSuchElementException:
                game_description = None
                print("Description not found")

            # Return result
            if title_element:
                return {
                    'title': game_title,
                    'score': int(score_text) if (score_text and score_text.isdigit()) else None,
                    'url': search_url,
                    'description': game_description,
                }
            return None

        except Exception as e:
            print(f"🚨 Error: {e}")
            return None

    def create_slug(self, title):
        """Convert the game title into a Metacritic-friendly slug."""
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)       # Remove special characters
        slug = re.sub(r'[-\s]+', '-', slug)        # Replace spaces with hyphens
        slug = slug.strip('-')                     # Trim hyphens at start and end
        return slug


class GameSpotScrapper():
    SEARCH_URL = "https://www.gamespot.com/games/"

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    } 

    def has_system_class(class_name):
        return class_name and 'system' in class_name

    def search_game(self, game_title):
        try:
            title_slug = self.create_slug(game_title)
            url = f"{self.SEARCH_URL}{title_slug}/"
            print(f"GameSpot'ta platform aranıyor: {game_title}")
            print(f"URL: {url}")

            response = requests.get(url, headers=self.HEADERS, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            platforms = []
            platform_list = soup.find('ul', class_='system-list')

            if platform_list:
                platform_items = platform_list.find_all('li', class_=self.has_system_class)

                for item in platform_items:
                    platform_span = item.find('span', itemprop="device")
                    if platform_span:
                        platform_name = platform_span.text.strip()
                        platforms.append(platform_name)

                print("Platform name(s) added")
                return {
                    'platforms': platforms,
                    'url': url,
                }
            else:
                print("No platform names found")
                return None

        except requests.exceptions.RequestException as e:
            print(f"HTTP Error: {e}")
            return None
        except Exception as e:
            print(f"General Error: {e}")
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
