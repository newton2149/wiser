from fastapi import  FastAPI
from src.configurations import lifespan

from src.utils import backend_router
from src.api import chat

app = FastAPI(lifespan=lifespan)
app.include_router(backend_router)
app.include_router(chat)



