import os
from dotenv import load_dotenv

load_dotenv(".venv/.env")

TOKEN = os.getenv("TOKEN")