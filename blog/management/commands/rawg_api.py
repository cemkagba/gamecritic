from django.core.management.base import BaseCommand
from blog.models import Game
from blog.rawg import RAWGAPIClient
import requests


from django.core.management.base import BaseCommand
from blog.models import Game
from blog.rawg import RAWGAPIClient
import requests


class Command(BaseCommand):
    help = 'Fetch cover images from RAWG API for games'
    
    def add_arguments(self, parser):
        parser.add_argument('--game-id', type=int, help='Specific game ID to fetch image')
        parser.add_argument('--game-title', type=str, help='Specific game title to fetch image')
        parser.add_argument('--all', action='store_true', help='Fetch images for all games')
        parser.add_argument('--search-term', type=str, help='Custom search term for RAWG API')
    
    def handle(self, *args, **options):
        client = RAWGAPIClient()
        
        if options['all']:
            self.fetch_all_images(client)
        elif options['game_id']:
            try:
                game = Game.objects.get(id=options['game_id'])
                search_term = options.get('search_term') or game.title
                self.fetch_game_image(client, game, search_term)
            except Game.DoesNotExist:
                self.stderr.write(self.style.ERROR(
                    f"Game with id={options['game_id']} not found."
                ))
                return
        elif options['game_title']:
            try:
                # Case-insensitive arama
                game = Game.objects.get(title__iexact=options['game_title'])
                search_term = options.get('search_term') or game.title
                self.fetch_game_image(client, game, search_term)
            except Game.DoesNotExist:
                self.stderr.write(self.style.ERROR(
                    f"Game with title='{options['game_title']}' not found."
                ))
                # Benzer başlıkları öner
                similar_games = Game.objects.filter(title__icontains=options['game_title'])[:5]
                if similar_games:
                    self.stdout.write("Similar games found:")
                    for game in similar_games:
                        self.stdout.write(f"  - {game.title} (ID: {game.id})")
                return
            except Game.MultipleObjectsReturned:
                games = Game.objects.filter(title__iexact=options['game_title'])
                self.stderr.write(self.style.ERROR(
                    f"Multiple games found with title '{options['game_title']}':"
                ))
                for game in games:
                    self.stdout.write(f"  - {game.title} (ID: {game.id})")
                return
        else:
            self.stderr.write(self.style.ERROR(
                "Please provide either --game-id, --game-title, or --all"
            ))
            return

    def fetch_all_images(self, client):
        """Tüm oyunlar için kapak fotoğrafı çek"""
        games = Game.objects.all()
        total = games.count()
        success_count = 0
        
        self.stdout.write(f"🚀 Starting to fetch images for {total} games...")
        
        for i, game in enumerate(games, 1):
            self.stdout.write(f"[{i}/{total}] Processing: {game.title}")
            
            if self.fetch_game_image(client, game):
                success_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Completed! {success_count}/{total} games updated with cover images."
            )
        )

    def fetch_game_image(self, client, game, search_term=None):
        """Tek oyun için kapak fotoğrafı çek"""
        search_name = search_term or game.title
        
        self.stdout.write(f"🔍 Searching: {search_name}")
        
        # Eğer zaten RAWG API'den fotoğraf varsa atla
        if game.img:
            self.stdout.write(
                self.style.WARNING(f"{game.title}: Already has RAWG image, skipping...")
            )
            return False
        
        success = client.update_game_image_url(game, search_name)
        
        if success:
            self.stdout.write(
                self.style.SUCCESS(f"✅ {game.title}: Image updated")
            )
            self.stdout.write(f"   📷 URL: {game.img}")
            return True
        else:
            self.stdout.write(
                self.style.WARNING(f"❌ {game.title}: No image found")
            )
            return False
