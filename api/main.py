from fastapi import FastAPI
from api.database import get_db_connection

app = FastAPI(title="Key-Value API")

@app.get("/")
def root():
    return {"message": "Key-Value API"}
