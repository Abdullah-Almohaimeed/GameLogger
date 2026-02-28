import os, webbrowser, psycopg2, signal
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from threading import Timer

load_dotenv(dotenv_path=r'C:\GameLogger\.env')

app = Flask(__name__, template_folder=r'C:\GameLogger\templates')

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, released, genres, platforms, user_rating, metacritic, playtime, beat, self_rating, date_added FROM games ORDER BY date_added DESC')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    games = [dict(zip(columns, row)) for row in rows]
    return render_template('index.html', games=games)

@app.route('/update/<int:game_id>', methods=['POST'])
def update(game_id):
    data = request.get_json()
    beat = data.get('beat') or None
    self_rating = data.get('self_rating') or None
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('UPDATE games SET beat = %s, self_rating = %s WHERE id = %s', (beat, self_rating, game_id))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        cur.close()
        conn.close()

@app.route('/delete/<int:game_id>', methods=['DELETE'])
def delete(game_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM games WHERE id = %s', (game_id,))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        cur.close()
        conn.close()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return jsonify({'success': True})

def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=False)