from django.core.management.base import BaseCommand
from blog.models import Game
from blog.utils.scrapers import MetacriticScraper
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Scrape Metacritic scores for games'
    
    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', help='Scrape all games')
        parser.add_argument('--game-id', type=int, help='Scrape a specific game by ID')
        parser.add_argument('--game-title', type=str, help='Scrape a specific game by title')
        
    def handle(self, *args, **options):
        scraper = MetacriticScraper()
        try:
            if options['all']:
                # Scrape all games from the database
                for game in Game.objects.all():
                    self.scrape_game_score(scraper, game)

            elif options['game_id']:
                try:
                    game = Game.objects.get(id=options['game_id'])
                    self.scrape_game_score(scraper, game)
                except Game.DoesNotExist:
                    self.stderr.write(self.style.ERROR(
                        f"Game with id={options['game_id']} not found."
                    ))

            elif options['game_title']:
                try:
                    game = Game.objects.get(title__iexact=options['game_title'])
                    self.scrape_game_score(scraper, game)
                except Game.DoesNotExist:
                    self.stderr.write(self.style.ERROR(
                        f"Game with title='{options['game_title']}' not found."
                    ))
                except Game.MultipleObjectsReturned:
                    games = Game.objects.filter(title__iexact=options['game_title'])
                    self.stderr.write(self.style.ERROR(
                        f"Multiple games found with title '{options['game_title']}':"
                    ))
                    for game in games:
                        self.stdout.write(f"  - {game.title} (ID: {game.id})")
            else:
                self.stderr.write(self.style.ERROR(
                    "Please provide either --all, --game-id or --game-title"
                ))
        finally:
            scraper.close()

    def scrape_game_score(self, scraper, game):
        """Scrape score and description for a given game and save it to DB."""
        self.stdout.write(f" Scraping: {game.title}")
        result = scraper.search_game(game.title)

        if result and result['score']:
            game.metaScore = result['score']
            if result.get('description'):
                game.description = result['description']
                self.stdout.write(f"Description updated")

            game.save()
            self.stdout.write(
                self.style.SUCCESS(f" {game.title}: {result['score']} saved")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f" {game.title}: No score found")
            )