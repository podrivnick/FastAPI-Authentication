import os

from dotenv import load_dotenv


load_dotenv()

POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

SECRET_KEY_AUTH = os.environ.get("SECRET_KEY_AUTH")

DEBUG = os.environ.get("DEBUG")

API_PORT = int(os.environ.get("API_PORT"))
API_HOST = os.environ.get("API_HOST")
