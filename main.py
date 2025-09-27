from fastapi import FastAPI
from database import get_db  # importa tu función real de la BD

from main import app, get_db

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "Hola, API funcionando 🚀"}
