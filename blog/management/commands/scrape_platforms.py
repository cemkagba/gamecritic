from django.core.management.base import BaseCommand
from blog.models import Game
from blog.utils.scrapers import GameSpotScrapper
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Scrape GameSpot platforms for games'
    
    def add_arguments(self, parser):

        parser.add_argument('--all', type=int, help='All games to scrape')        
        parser.add_argument('--game-id', type=int, help='Specific game ID to scrape')
        parser.add_argument('--game-title', type=str, help='Specific game title to scrape')
        
    def handle(self, *args, **options):
        scraper = GameSpotScrapper()

        if options['all']:
            games = Game.objects.all()
            for game in games:
                self.scrape_platform(scraper,game)


        if options['game_id']:
            try:
                game = Game.objects.get(id=options['game_id'])
                self.scrape_platform(scraper, game)
            except Game.DoesNotExist:
                self.stderr.write(self.style.ERROR(
                    f"Game with id={options['game_id']} not found."
                ))
                return

        elif options['game_title']:
            try:
                # Case-insensitive arama
                game = Game.objects.get(title__iexact=options['game_title'])
                self.scrape_platform(scraper, game) 
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
                "Please provide either --game-id or --game-title"
            ))
            return

    def scrape_platform(self, scraper, game):
        self.stdout.write(f" Scraping: {game.title}")
        result = scraper.search_game(game.title)

        if result and result.get('platforms'):

            platforms_str = ', '.join(result['platforms'])
            game.platform = platforms_str
            game.save()
            self.stdout.write(
                self.style.SUCCESS(f" {game.title}: {platforms_str} saved")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f" {game.title}: No platform found")
            )
