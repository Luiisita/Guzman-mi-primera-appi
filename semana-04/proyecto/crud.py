from sqlalchemy.orm import Session
from sqlalchemy import or_
import models, schemas

def crear_producto(db: Session, producto: schemas.ProductoCreate):
    """Crear un nuevo producto"""
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def obtener_producto(db: Session, producto_id: int):
    """Obtener producto por ID"""
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()

def obtener_productos(db: Session, skip: int = 0, limit: int = 10):
    """Obtener lista de productos con paginación"""
    return db.query(models.Producto).offset(skip).limit(limit).all()

def buscar_productos(db: Session, busqueda: str):
    """Buscar productos por nombre o descripción"""
    return db.query(models.Producto).filter(
        or_(
            models.Producto.nombre.contains(busqueda),
            models.Producto.descripcion.contains(busqueda)
        )
    ).all()

def actualizar_producto(db: Session, producto_id: int, producto: schemas.ProductoUpdate):
    """Actualizar producto existente"""
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto:
        # Solo actualizar campos que no sean None
        update_data = producto.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_producto, field, value)
        db.commit()
        db.refresh(db_producto)
    return db_producto

def eliminar_producto(db: Session, producto_id: int):
    """Eliminar producto"""
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto:
        db.delete(db_producto)
        db.commit()
    return db_producto

def contar_productos(db: Session):
    """Contar total de productos"""
    return db.query(models.Producto).count()