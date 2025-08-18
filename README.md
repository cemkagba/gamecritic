
# GameCritic

GameCritic is a Django-based web application for reviewing, rating, and discussing games with a community.

## Features
- User registration and login
- Add, edit, and delete games
- Rate and comment on games
- Blog and news module
- YouTube and RAWG API integration
- Modern and responsive interface

## Installation
1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure your database settings in the `.env` file.
3. To start with Docker:
   ```bash
   docker-compose up --build
   ```
4. Collect static files:
   ```bash
   python manage.py collectstatic
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```

## Contribution
Please fork the repository and submit a pull request to contribute.

## License
This project is licensed under the MIT License.
