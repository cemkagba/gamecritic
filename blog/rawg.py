import requests
import os
from dotenv import load_dotenv

class RAWGAPIClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("RAWG_API_KEY")
        self.base_url = "https://api.rawg.io/api"
    
    def search_game(self, game_name):
        """Search for game and return first result"""
        url = f"{self.base_url}/games"
        params = {
            'search': game_name,
            'page_size': 1
        }
        
        # Add API key if available
        if self.api_key:
            params['key'] = self.api_key
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            
            if data['results']:
                return data['results'][0]
            return None
        except requests.RequestException as e:
            print(f"API Error: {e}")
            return None
    
    def update_game_image_url(self, game_instance, game_name=None):
        """Update the game's img indicator with the image link from the RAWG API"""
        search_name = game_name or game_instance.title
        rawg_game = self.search_game(search_name)
        
        if not rawg_game or not rawg_game.get('background_image'):
            return False
        
        # Update the img field with the link from the API
        game_instance.img = rawg_game['background_image']
        game_instance.save()
        
        print(f"Updated {game_instance.title} with image: {game_instance.img}")
        return True
