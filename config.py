import os
from dotenv import load_dotenv

load_dotenv(".venv/.env")

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

TOKEN_MINECRAFT_TOKEN = os.getenv("TOKEN_MINECRAFT_HOSTING")

MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
ENGINE = 'sqlite+aiosqlite:///app/database/data.sqlite3'
ECHO = True

RCON_IP = os.getenv("RCON_IP")
RCON_PASSWORD = os.getenv("RCON_PASSWORD")
RCON_PORT = os.getenv("RCON_PORT")