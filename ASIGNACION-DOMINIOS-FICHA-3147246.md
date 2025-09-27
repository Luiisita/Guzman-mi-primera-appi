# 🚀 FICHA 3147246 - ASIGNACIÓN DE DOMINIOS SEMANA 6

## 👥 **ASIGNACIÓN DE DOMINIOS ÚNICOS POR ESTUDIANTE**

| Apellido           | Dominio               | Entidad Principal | Prefijo Test | Módulo Test     |
| ------------------ | --------------------- | ----------------- | ------------ | --------------- |
| AMAYA BEJARANO     | **Clínica Dental**    | paciente          | `dental_`    | `test_dental`   |
| BAYONA RODRIGUEZ   | **Centro Estético**   | tratamiento       | `estetica_`  | `test_estetica` |
| BERNAL RODRIGUEZ   | **Laboratorio**       | muestra           | `lab_`       | `test_lab`      |
| BOHORQUEZ MEDINA   | **Autolavado**        | servicio          | `wash_`      | `test_wash`     |
| CARO CASTILLO      | **Fotografía**        | sesion            | `photo_`     | `test_photo`    |
| DIAZ SARMIENTO     | **Eventos**           | evento            | `event_`     | `test_event`    |
| DUQUE URIBE        | **Mascotas Grooming** | cita              | `groom_`     | `test_groom`    |
| GAONA PRADA        | **Catering**          | menu              | `catering_`  | `test_catering` |
| GUZMAN ALVAREZ     | **Spa**               | reserva           | `spa_`       | `test_spa`      |
| GUZMAN GARZON      | **Academia Música**   | clase             | `music_`     | `test_music`    |
| GUZMAN MARTINEZ    | **Rent a Car**        | alquiler          | `rental_`    | `test_rental`   |
| LADINO MARTINEZ    | **Funeraria**         | servicio          | `funeral_`   | `test_funeral`  |
| LEON ROLDAN        | **Courier**           | envio             | `courier_`   | `test_courier`  |
| MARTINEZ CARDENAS  | **Seguridad**         | guardia           | `security_`  | `test_security` |
| MEDINA VARGAS      | **Jardinería**        | proyecto          | `garden_`    | `test_garden`   |
| MOSQUERA ABADIA    | **Plomería**          | reparacion        | `plumber_`   | `test_plumber`  |
| NAVAS LOPEZ        | **Electricidad**      | instalacion       | `electric_`  | `test_electric` |
| OLAYA RIOS         | **Lavandería**        | pedido            | `laundry_`   | `test_laundry`  |
| PRATO BARON        | **Mudanzas**          | traslado          | `moving_`    | `test_moving`   |
| QUINTERO MARTINEZ  | **Diseño Gráfico**    | proyecto          | `design_`    | `test_design`   |
| RAMOS GOMEZ        | **Carpintería**       | mueble            | `wood_`      | `test_wood`     |
| RODRIGUEZ MARTINEZ | **Academia Baile**    | inscripcion       | `dance_`     | `test_dance`    |
| ROJAS BURBANO      | **Psicología**        | consulta          | `psych_`     | `test_psych`    |
| SANCHEZ CASTAÑO    | **Nutrición**         | plan              | `nutri_`     | `test_nutri`    |
| SANDON GUARIN      | **Cerrajería**        | trabajo           | `keys_`      | `test_keys`     |
| SEGURA CONTRERAS   | **Academia Idiomas**  | curso             | `lang_`      | `test_lang`     |
| TEQUIA FORERO      | **Limpieza**          | contrato          | `clean_`     | `test_clean`    |
| ZAZIPA SIMBAQUEBA  | **Reparación PC**     | diagnostico       | `tech_`      | `test_tech`     |

---

## 📋 **INSTRUCCIONES ESPECÍFICAS PARA SEMANA 6 - TESTING**

### **🚨 REGLAS OBLIGATORIAS**

1. **❌ PROHIBIDO COPIAR Y PEGAR** tests de compañeros
2. **✅ CADA ESTUDIANTE** debe usar SU dominio específico
3. **📝 TODOS LOS TESTS** deben reflejar su negocio
4. **🔍 REVISIÓN INDIVIDUAL** de cobertura y tests por dominio

### **📝 Estructura de Testing Personalizada**

Cada estudiante debe crear tests específicos para su dominio:

#### **Ejemplo: AMAYA BEJARANO - Clínica Dental**

```python
# test_dental.py
import pytest
from fastapi.testclient import TestClient

class TestDentalAPI:
    def test_create_paciente(self, client):
        data = {
            "nombre": "María González",
            "edad": 35,
            "telefono": "3001234567",
            "historial_medico": "Sin alergias conocidas",
            "tipo_sangre": "O+",
            "contacto_emergencia": "3007654321"
        }
        response = client.post("/dental/pacientes/", json=data)
        assert response.status_code == 201
        assert response.json()["nombre"] == "María González"

    def test_get_paciente_not_found(self, client):
        response = client.get("/dental/pacientes/999")
        assert response.status_code == 404
        assert "Paciente no encontrado" in response.json()["detail"]
```

#### **Ejemplo: BAYONA RODRIGUEZ - Centro Estético**

```python
# test_estetica.py
import pytest
from fastapi.testclient import TestClient

class TestEsteticaAPI:
    def test_create_tratamiento(self, client):
        data = {
            "cliente": "Laura Martínez",
            "tipo_tratamiento": "Limpieza facial",
            "duracion_minutos": 60,
            "precio": 80000,
            "productos_usados": ["Exfoliante", "Mascarilla"],
            "observaciones": "Piel grasa"
        }
        response = client.post("/estetica/tratamientos/", json=data)
        assert response.status_code == 201
        assert response.json()["tipo_tratamiento"] == "Limpieza facial"

    def test_precio_invalido(self, client):
        data = {"duracion_minutos": 0}  # Duración inválida
        response = client.post("/estetica/tratamientos/", json=data)
        assert response.status_code == 422
```

---

## 🎯 **ESPECIFICACIONES POR DOMINIO**

### **🦷 Clínica Dental (AMAYA BEJARANO)**

- **Entidad**: Paciente dental
- **Campos**: nombre, edad, historial_medico, tipo_sangre, contacto_emergencia
- **Tests específicos**: Validar historial médico, alergias, emergencias

### **💄 Centro Estético (BAYONA RODRIGUEZ)**

- **Entidad**: Tratamiento estético
- **Campos**: cliente, tipo_tratamiento, duracion_minutos, precio, productos_usados
- **Tests específicos**: Validar precios, duración, productos

### **🧪 Laboratorio (BERNAL RODRIGUEZ)**

- **Entidad**: Muestra de laboratorio
- **Campos**: paciente, tipo_muestra, fecha_toma, resultados, observaciones
- **Tests específicos**: Validar tipos de muestra, resultados, fechas

### **🚗 Autolavado (BOHORQUEZ MEDINA)**

- **Entidad**: Servicio de lavado
- **Campos**: vehiculo, tipo_lavado, precio, tiempo_estimado, extras
- **Tests específicos**: Validar tipos de vehículo, servicios, precios

_[Continúa para todos los 28 dominios...]_

---

## 📊 **CONTROL DE CALIDAD FICHA 3147246**

### **Verificación Automática**

- Cada commit se revisa por prefijo de test
- Código duplicado se detecta automáticamente
- Cobertura se mide por módulo personalizado

### **Evaluación Individual**

- **30%** Tests específicos del dominio
- **25%** Cobertura >80% módulo personal
- **20%** Casos de error únicos
- **15%** Estructura profesional
- **10%** Documentación

---

## 🚨 **IMPORTANTE PARA FICHA 3147246**

**✅ Cada dominio es ÚNICO e IRREPETIBLE**  
**✅ Los tests deben reflejar la LÓGICA ESPECÍFICA de su negocio**  
**✅ NO se pueden intercambiar dominios entre estudiantes**  
**✅ La evaluación es 100% PERSONALIZADA**

**🎯 ¡Al final cada uno será experto en testing para su industria específica!**
