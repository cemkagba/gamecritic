docker-compose run --rm web python manage.py scrape_metascore --all 
docker-compose run --rm web python manage.py scrape_platforms --all 1
docker-compose run --rm web python manage.py rawg_api --all