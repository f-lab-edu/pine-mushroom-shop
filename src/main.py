from contextlib import asynccontextmanager

import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from src.core import config
from src.apis.common import common_router
from src.apis import router as api_router
from src.core.database import close_db, create_db_and_tables
from src.core.middleware import LoggingMiddleWare

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)
add_pagination(app)
app.include_router(common_router)
app.include_router(api_router)
app.add_middleware(LoggingMiddleWare)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors.origins.split(","),
    allow_credentials=True,
    allow_methods=config.cors.methods.split(","),
    allow_headers=config.cors.headers.split(","),
)


if __name__ == "__main__":
    uvicorn.run(app, host=config.web.host, port=config.web.port)
