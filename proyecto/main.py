from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, get_db
from sqlalchemy import text

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="API Productos Mejorada")

# CREATE - Crear producto con validaciones
@app.post("/productos/", response_model=schemas.Producto)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    try:
        return crud.crear_producto(db=db, producto=producto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# READ - Listar productos con paginación
@app.get("/productos/")
def listar_productos(
    skip: int = Query(0, ge=0, description="Saltar elementos"),
    limit: int = Query(10, ge=1, le=100, description="Límite de elementos"),
    db: Session = Depends(get_db)
):
    productos = crud.obtener_productos(db, skip=skip, limit=limit)
    total = crud.contar_productos(db)
    return {
        "productos": productos,
        "total": total,
        "pagina": skip // limit + 1,
        "por_pagina": limit
    }

# READ - Buscar productos
@app.get("/productos/buscar/")
def buscar_productos(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    db: Session = Depends(get_db)
):
    productos = crud.buscar_productos(db, busqueda=q)
    return {
        "busqueda": q,
        "productos": productos,
        "total": len(productos)
    }

# READ - Obtener producto por ID
@app.get("/productos/{producto_id}", response_model=schemas.Producto)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = crud.obtener_producto(db, producto_id=producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# UPDATE - Actualizar producto parcialmente
@app.patch("/productos/{producto_id}", response_model=schemas.Producto)
def actualizar_producto(
    producto_id: int,
    producto: schemas.ProductoUpdate,
    db: Session = Depends(get_db)
):
    db_producto = crud.actualizar_producto(db, producto_id=producto_id, producto=producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# DELETE - Eliminar producto
@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = crud.eliminar_producto(db, producto_id=producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": f"Producto {producto_id} eliminado correctamente"}

# STATS - Estadísticas básicas
@app.get("/productos/stats/resumen")
def estadisticas_productos(db: Session = Depends(get_db)):
    total = crud.contar_productos(db)
    productos = crud.obtener_productos(db, limit=total)

    if not productos:
        return {"total": 0, "precio_promedio": 0, "precio_max": 0, "precio_min": 0}

    precios = [p.precio for p in productos]
    return {
        "total": total,
        "precio_promedio": sum(precios) / len(precios),
        "precio_max": max(precios),
        "precio_min": min(precios)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    
@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    """Endpoint para probar la conexión a la base de datos"""
    try:
        # Realizar una consulta simple
        result = db.execute(text("SELECT 1")).fetchone()
        return {"database": "connected", "test_query": result[0]}
    except Exception as e:
        return {"database": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)