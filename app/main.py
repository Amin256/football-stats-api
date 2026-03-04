from fastapi import FastAPI
from .database import engine
from . import models
from .routers import teams

models.Base.metadata.create_all(bind = engine)

app = FastAPI(
    title = "Football Stats API",
    description = "REST API for football match statistics and analytics",
    version = "1.0"
)

app.include_router(teams.router)

@app.get("/")
def root():
    return {"message": "Football Stats API is running"}