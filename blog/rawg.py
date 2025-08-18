import requests
from .models import Game

class RAWGAPIClient:
    def __init__(self):
        
        self.api_key = "526549ab6f07446f8e785153b4809445"
        self.base_url = "https://api.rawg.io/api"
    
    def search_game(self, game_name):
        """Oyun ara ve ilk sonucu döndür"""
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
            response.raise_for_status()
            data = response.json()
            
            if data['results']:
                return data['results'][0]
            return None
        except requests.RequestException as e:
            print(f"API Error: {e}")
            return None
    
    def update_game_image_url(self, game_instance, game_name=None):
        """Oyunun img alanını RAWG API'dan gelen fotoğraf linki ile güncelle"""
        search_name = game_name or game_instance.title
        rawg_game = self.search_game(search_name)
        
        if not rawg_game or not rawg_game.get('background_image'):
            return False
        
        # img alanını API'dan gelen link ile güncelle
        game_instance.img = rawg_game['background_image']
        game_instance.save()
        
        print(f"Updated {game_instance.title} with image: {game_instance.img}")
        return True
