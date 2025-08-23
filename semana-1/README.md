# Mi Primera API FastAPI - Bootcamp

**👤 Desarrollador**: Luisa Guzman
**📧 Email**: “Luiisita@users.noreply.github.com”
**� Privacidad**: Email configurado según mejores prácticas de GitHub
**�📅 Fecha de creación**: 2025-08-07 00:36:39
**📂 Ruta del proyecto**: /c/Users/ireap/luisa-guzman/semana-1/mi-primera-fastapi
**💻 Equipo de trabajo**: iReaperOff

## 🔧 Configuración Local

Este proyecto está configurado para trabajo en equipo compartido:

- **Entorno virtual aislado**: `venv-personal/`
- **Configuración Git local**: Solo para este proyecto
- **Dependencias independientes**: No afecta otras instalaciones

## 🚀 Instalación y Ejecución

```bash
# 1. Activar entorno virtual personal
source venv-personal/bin/activate

# 2. Instalar dependencias (si es necesario)
pip install -r requirements.txt

# 3. Ejecutar servidor de desarrollo
uvicorn main:app --reload --port 8000
```

## 📝 Notas del Desarrollador

- **Configuración Git**: Local únicamente, no afecta configuración global
- **Email de GitHub**: Configurado con email privado para proteger información personal
- **Entorno aislado**: Todas las dependencias en venv-personal/
- **Puerto por defecto**: 8000 (cambiar si hay conflictos)
- **Estado del bootcamp**: Semana 1 - Configuración inicial

## 🛠️ Troubleshooting Personal

- Si el entorno virtual no se activa: `rm -rf venv-personal && python3 -m venv venv-personal`
- Si hay conflictos de puerto: cambiar --port en uvicorn
- Si Git no funciona: verificar `git config user.name` y `git config user.email`
- Si necesitas cambiar el email: usar el email privado de GitHub desde Settings → Emails




# Mi Primera API FastAPI

## ¿Qué hace?

Una API básica creada en el Bootcamp FastAPI Semana 1.

## ¿Cómo ejecutar?

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Endpoints
- /: Mensaje de bienvenida

- /info : Información de la API

- /my-profile : Mi perfil personal

## Reflexion
[Escribe 2-3 oraciones sobre qué aprendiste]
- Aprendi nuevas terminos (endpoints, crear carpetas desde la terminal), y tambien reforce practicas como el crear un entorno y activarlo.
- Aunque se me dificulto un poco la conexion para que apareciera en el navegador


3. **Subir a GitHub** (paso a paso con instructor):
   - Crear repositorio: `tu-apellido-primera-api`
   - `git init`
   - `git add .`
   - `git commit -m "Mi primera API FastAPI"`
   - `git push`

### ✅ Criterio de Éxito
- Repositorio en GitHub con 3 archivos mínimos
- README se ve bien en GitHub

---

## 🚨 Si tienes problemas

**NO te compliques**. Este bloque es para consolidar, no para frustrarse.

### Problemas comunes:
- **Git no funciona**: El instructor te ayudará
- **Endpoint no responde**: Revisar sintaxis del código
- **No sale en /docs**: Reiniciar uvicorn

### Solución rápida:
- Levanta la mano
- Pide ayuda a un compañero
- Enfócate en lo que SÍ funciona

---

## 🎯 Resultado Final (Lo que deberías tener)

Al final del Bloque 3:

1. **✅ API con 3-4 endpoints funcionando**
2. **✅ Código en GitHub**
3. **✅ README básico**
4. **✅ Sensación de logro**

### 📁 Estructura Final Mínima

```
semana-1/mi-primera-fastapi/
 ├── main.py # Tu API 
 ├── requirements.txt #Dependencias 
 └── README.md # Documentaciónbásica

```
---

## 📊 Auto-evaluación (1 minuto)

**¿Lograste crear tu primera API?** ✅ Sí / ❌ No

**¿Está funcionando /docs?** ✅ Sí / ❌ No

**¿Está en GitHub?** ✅ Sí / ❌ No

**Si respondiste 2/3 "Sí": ¡EXCELENTE!**
**Si respondiste 1/3 "Sí": ¡MUY BIEN!**
**Si respondiste 0/3 "Sí": ¡El instructor te ayudará!**

---

## 🚀 Preparación para Semana 2

Con estos ejercicios básicos completados, en la Semana 2 estarás listo para:

- **Python Type Hints** (conceptos que ya usaste sin saberlo)
- **Pydantic Models** (para datos más estructurados)
- **Más tipos de endpoints** (POST, PUT, DELETE básicos)

**¡Felicidades por completar tu primera semana! 🎉**






# Mi API FastAPI - Semana 2
## ¿Qué hace?

API mejorada con validación automática de datos y type hints.

## Nuevos Features (Semana 2)

- ✅ Type hints en todas las funciones
- ✅ Validación automática con Pydantic
- ✅ Endpoint POST para crear datos
- ✅ Parámetros de ruta (ejemplo: /products/{id})
- ✅ Búsqueda con parámetros query

## ¿Cómo ejecutar?

```bash
pip install fastapi pydantic uvicorn
uvicorn main:app --reload
```

## Reflexion Practica

¿Cómo mejoraron estos conceptos tu API comparada con Semana 1?,
Anota 2-3 oraciones para tu README.
RTA: 

- Queedaron mas claros algunos conceptos y las practicas hacen que se mas rapido el proceso.


**2. Subir a GitHub** (10 min):

```bash
# En tu terminal, en la carpeta de tu proyecto
git add .
git commit -m "Semana 2: API con Pydantic y Type Hints"
git push