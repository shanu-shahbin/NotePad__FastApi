from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.note import router as notes_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(notes_router, prefix="/notes")

@app.get("/")
def home():
    return {
        "message": "Welcome to the Notes API",
        "status": "success",
        "version": "1.0",
        "description": "A RESTful API for managing personal notes",
        "endpoints": {
            "auth": "/auth - Authentication endpoints",
            "notes": "/notes - Notes management endpoints"
        }
    }