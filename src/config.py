from os import getenv, path
from dotenv import load_dotenv

dirname = path.dirname(__file__)
envfile_path = path.join(dirname, "..", ".env")

if path.exists(envfile_path):
    load_dotenv(envfile_path)

DATABASE_URL = getenv("DATABASE_URL")
SECRET_KEY = getenv("SECRET_KEY")
