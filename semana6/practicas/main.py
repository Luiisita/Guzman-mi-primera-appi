# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from practicas.database import Base, engine, get_db
from pydantic import BaseModel

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Spa API - Gestión de Reservas")

# ==========================
# MODELO Pydantic (entrada)
# ==========================
class ReservaCreate(BaseModel):
    campo1: str
    campo2: str

# ==========================
# MODELO ORM (BD)
# ==========================
from sqlalchemy import Column, Integer, String

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    campo1 = Column(String, index=True)
    campo2 = Column(String, index=True)

# ==========================
# RUTAS
# ==========================
@app.post("/spa_reservas/", status_code=201)
def create_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    # Validación simple: campo1 no vacío
    if not reserva.campo1:
        raise HTTPException(status_code=422, detail="campo1 es requerido")

    # Validar duplicados (ejemplo: campo1 único)
    existing = db.query(Reserva).filter(Reserva.campo1 == reserva.campo1).first()
    if existing:
        raise HTTPException(status_code=400, detail="Reserva ya existe")

    new_reserva = Reserva(campo1=reserva.campo1, campo2=reserva.campo2)
    db.add(new_reserva)
    db.commit()
    db.refresh(new_reserva)
    return new_reserva

@app.get("/spa_reservas/{reserva_id}")
def get_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="reserva no encontrado")
    return reserva

@app.get("/spa_reservas/")
def get_reservas(db: Session = Depends(get_db)):
    return db.query(Reserva).all()
