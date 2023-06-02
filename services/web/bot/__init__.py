from fastapi import FastAPI
from .config import config

app = FastAPI(docs_url=None, redoc_url=None)

if app:
    from .common import routes
