from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes import controllers, token, users, darpal
from app.core.config import ALLOWED_HOSTS, API_V1_STR, PROJECT_NAME, PROJECT_DESCRIPTION
from app.db.mongodb_utils import close_mongo_connection, connect_to_mongo

app = FastAPI(
    title=PROJECT_NAME,
    version='0.0.1',
    description=PROJECT_DESCRIPTION,
    license={
        'name': 'European Union Public License 1.2',
        'url': 'https://spdx.org/licenses/EUPL-1.2.html',
    },
)

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Origin"],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(darpal.router)
app.include_router(controllers.router)
app.include_router(users.router)
app.include_router(token.router)