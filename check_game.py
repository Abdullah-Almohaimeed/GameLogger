import sys, os, requests, psycopg2, logging
from dotenv import load_dotenv

load_dotenv(dotenv_path=r'C:\GameLogger\.env')

API_KEY = os.getenv('RAWG_API_KEY')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(r'C:\GameLogger\gamelogger.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

def get_game_name():
    file_name = ' '.join(sys.argv[1:])
    name_only = os.path.basename(file_name)
    cleaned = os.path.splitext(name_only)[0]
    return cleaned

def get_game_info(query):
    url = 'https://api.rawg.io/api/games'
    params = {
        'key': API_KEY,
        'page_size': 1,
        'search': query,
        'page': 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results')
        if results:
            game = results[0]
            genres = ', '.join([g['name'] for g in game.get('genres', [])])
            platforms = ', '.join([p['platform']['name'] for p in game.get('platforms', [])])
            released = game.get('released', '')[:4] if game.get('released') else None
            return {
                'name': game.get('name'),
                'released': released,
                'genres': genres,
                'platforms': platforms,
                'rating': game.get('rating'),
                'metacritic': game.get('metacritic'),
                'playtime': game.get('playtime')
            }
        else:
            logger.warning(f"No results found for query: {query}")
            return None
    else:
        logger.error(f"API request failed with status code: {response.status_code}")
        return None

def save_to_db(game_info):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO games (name, released, genres, platforms, user_rating, metacritic, playtime)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            game_info['name'],
            game_info['released'],
            game_info['genres'],
            game_info['platforms'],
            game_info['rating'],
            game_info['metacritic'],
            game_info['playtime']
        ))
        conn.commit()
        return True
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return False
    except Exception as e:
        logger.error(f"Database error: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def run():
    game_name = get_game_name()
    logger.info(f"Looking up: {game_name}")
    info = get_game_info(game_name)
    if not info:
        logger.warning("Game not found.")
        return
    if not save_to_db(info):
        logger.warning(f"{info['name']} already exists in the database.")
        return
    logger.info(f"Added: {info['name']} ({info['released']})")
    logger.info(f"Genres: {info['genres']}")
    logger.info(f"Platforms: {info['platforms']}")
    logger.info(f"Rating: {info['rating']} | Metacritic: {info['metacritic']} | Avg Playtime: {info['playtime']}hrs")

run()