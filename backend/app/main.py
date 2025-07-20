"""Main application file for the FastAPI backend."""
from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/")
async def root():
    """Root endpoint for the API."""
    return {"message": "Hello World"}
