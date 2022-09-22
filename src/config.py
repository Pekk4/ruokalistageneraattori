from os import getenv, path, mkdir
from dotenv import load_dotenv


dirname = path.dirname(__file__)
envfile_path = path.join(dirname, "..", ".env")
logfiles_path = path.join(dirname, "..", "logs")

if path.exists(envfile_path):
    load_dotenv(envfile_path)

if not path.exists(logfiles_path):
    mkdir(logfiles_path)

DATABASE_URL = getenv("DATABASE_URL")
SECRET_KEY = getenv("SECRET_KEY")
LOGGER_CONFIG_FILE = getenv("LOGGER_CONFIG_FILE")
