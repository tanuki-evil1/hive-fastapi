from fastapi import FastAPI

from app.api.endpoints.user import router as user_router
from app.api.endpoints.event import router as event_router

app = FastAPI()

app.include_router(user_router)
app.include_router(event_router)
