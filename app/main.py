from fastapi import FastAPI

app = FastAPI(
    title = "Football Stats API",
    description = "REST API for football match statistics and analytics",
    version = "1.0"
)

@app.get("/")
def root():
    return {"message": "Football Stats API is running"}