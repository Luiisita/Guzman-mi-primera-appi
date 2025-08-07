#!/usr/bin/env python3
"""
Mi Primera API FastAPI - Verificación de Setup
Desarrollador: [Tu nombre se llenará automáticamente]
"""

from fastapi import FastAPI
import os
import sys
from datetime import datetime

# Crear instancia de FastAPI
app = FastAPI(
    title="Mi Primera API FastAPI",
    description="API de verificación para setup del bootcamp",
    version="1.0.0"
)

@app.get("/")
def home():
    """Endpoint principal de verificación"""
    return {
        "message": "¡Setup completado correctamente!",
        "project": "FastAPI Bootcamp - Semana 1",
        "timestamp": datetime.now().isoformat(),
        "status": "✅ Working perfectly"
    }@app.get("/info/setup")
def info_setup():
    """Información del entorno de desarrollo"""
    return {
        "python_version": sys.version,
        "python_path": sys.executable,
        "working_directory": os.getcwd(),
        "virtual_env": os.environ.get("VIRTUAL_ENV", "No detectado"),
        "user": os.environ.get("USER", "No detectado"),
        "hostname": os.environ.get("HOSTNAME", "No detectado")
    }

@app.get("/health")
def health_check():
    """Endpoint de verificación de salud"""
    return {
        "status": "healthy",
        "message": "API running correctly",
        "environment": "development"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor de verificación...")
    print("📍 Acceder a: http://localhost:8000")
    print("📖 Documentación: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
