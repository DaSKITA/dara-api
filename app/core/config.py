import os
import json

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret
from databases import DatabaseURL


API_V1_STR = "/api"

load_dotenv(".env")

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
SECRET_KEY = Secret(os.getenv("SECRET_KEY", "secret key for project"))

API_USERNAME = Secret(os.getenv("API_USERNAME", "api_name"))
API_PASSWORD = Secret(os.getenv("API_PASSWORD", "api_password"))
USER_DB = json.loads(os.getenv("USER_DB", "{}"))

API_SECRET_KEY = str(os.getenv("API_SECRET_KEY", "secret key"))
API_ALGORITHM = os.getenv("API_ALGORITHM", "HS256")
API_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("API_ACCESS_TOKEN_EXPIRE_MINUTES", 30))

PROJECT_NAME = os.getenv("PROJECT_NAME", "")
PROJECT_DESCRIPTION = os.getenv("PROJECT_DESCRIPTION", "")
ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))

MONGODB_URL = os.getenv("MONGODB_URL", "")  # deploying without docker-compose
MONGO_INITDB_DATABASE = os.getenv("MONGO_INITDB_DATABASE", "api")

if not MONGODB_URL:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER = os.getenv("MONGO_USER", "userdb")
    MONGO_PASS = os.getenv("MONGO_PASSWORD", "pass")

    MONGODB_URL = DatabaseURL(
        f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_INITDB_DATABASE}"
    )
else:
    MONGODB_URL = DatabaseURL(MONGODB_URL)


database_name = MONGO_INITDB_DATABASE

controller_collection: str = "controllers"
darpal_collection: str = "darpal"