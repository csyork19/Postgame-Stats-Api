from flask import Flask
from flask_cors import CORS
import logging

import sqlite3
from routes.auth import auth_bp
from routes.cbb import ncaa_mens_team_bp
from routes.gleague import gleague_player_bp
from routes.nba import nba_player_bp, nba_team_bp
from routes.nfl import nfl_player_bp
from routes.wnba import wnba_player_bp

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=logging.DEBUG,  # or INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s [%(levelname)s] %(message)s',
)

SECRET_KEY = "my_dirty_little_secret"  # All American Rejects :)


def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()


def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "my_dirty_little_secret" # All American Rejects :)

    # Register blueprints
    app.register_blueprint(nba_player_bp)
    app.register_blueprint(nba_team_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(nfl_player_bp)
    app.register_blueprint(ncaa_mens_team_bp)
    app.register_blueprint(gleague_player_bp)
    app.register_blueprint(wnba_player_bp)
    app.run(host="0.0.0.0", port=5000)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
