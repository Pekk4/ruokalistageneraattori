from os import getenv, path
from dotenv import load_dotenv


dirname = path.dirname(__file__)
envfile_path = path.abspath(path.join(dirname, "..", ".env"))
logfiles_path = path.abspath(path.join(dirname, "..", "logs"))

if path.exists(envfile_path):
    load_dotenv(envfile_path)

DATABASE_URL = getenv("DATABASE_URL")
SECRET_KEY = getenv("SECRET_KEY")
LOGGER_CONFIG_FILE = getenv("LOGGER_CONFIG_FILE")
CSP = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'data:',
    ]
}
