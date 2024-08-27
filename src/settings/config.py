import os

from dotenv import load_dotenv


load_dotenv()

DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = os.environ.get("DATABASE_PORT")

SECRET_KEY_AUTH = os.environ.get("SECRET_KEY_AUTH")

DEBUG = os.environ.get("DEBUG")

API_PORT = int(os.environ.get("API_PORT"))
API_HOST = os.environ.get("API_HOST")
