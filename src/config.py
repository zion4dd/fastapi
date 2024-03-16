import os

from dotenv import load_dotenv

load_dotenv(".dev.env", override=True)

DB_URL = os.environ.get("DB_URL")
SECRET_AUTH = os.environ.get("SECRET_AUTH")
REDIS_URL = os.environ.get("REDIS_URL")
