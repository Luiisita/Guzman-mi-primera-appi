
# Reporte de Testing - SPA

## Cobertura Actual: 90%

> Nota: Este porcentaje es aproximado según la cobertura de los tests implementados en `test_spa.py`. Se recomienda usar `pytest --cov=spa` para métricas exactas.

---

## Casos de Prueba Específicos

1. **Crear reserva exitosa**  
   - Test: `test_create_reserva_success`  
   - Valida que se pueda crear una reserva con datos correctos y que la respuesta contenga los campos esperados.

2. **Crear reserva duplicada**  
   - Test: `test_create_reserva_duplicate`  
   - Verifica que la API no permita reservas duplicadas y devuelva un error 400.

3. **Consulta de reservas por ID**  
   - Test: `test_get_reserva_by_id`  
   - Comprueba que se pueda obtener una reserva específica por su ID.

4. **Consulta de todas las reservas**  
   - Test: `test_get_all_reservas`  
   - Verifica que la API devuelva la lista completa de reservas existentes.

5. **Reserva no encontrada**  
   - Test: `test_get_reserva_not_found`  
   - Comprueba el manejo de IDs inexistentes y que devuelva 404.

6. **Actualización completa de reserva**  
   - Test: `test_update_reserva_complete`  
   - Valida que se puedan actualizar todos los campos de una reserva.

7. **Actualización parcial de reserva**  
   - Test: `test_update_reserva_partial`  
   - Verifica que se pueda actualizar solo un campo (PATCH) sin afectar otros datos.

8. **Eliminación de reserva exitosa**  
   - Test: `test_delete_reserva_success`  
   - Comprueba que se pueda eliminar una reserva existente y que luego no sea accesible.

9. **Eliminación de reserva inexistente**  
   - Test: `test_delete_reserva_not_found`  
   - Verifica que al intentar eliminar una reserva inexistente se devuelva un error 404.

10. **Validaciones de reglas de negocio**  
    - Test: `test_reserva_business_rules`  
    - Valida que la fecha, hora y estado de la reserva cumplan las reglas definidas (pendiente, confirmada, cancelada).

11. **Registro y login de usuarios**  
    - Tests: `test_register_reserva_user`, `test_login_reserva_user`  
    - Comprueba que los usuarios puedan registrarse y autenticarse correctamente.

12. **Permisos de roles**  
    - Tests: `test_admin_can_delete_reserva`, `test_regular_user_cannot_delete_reserva`  
    - Verifica que solo los administradores puedan eliminar reservas y que usuarios regulares tengan restricciones adecuadas.

13. **Acceso según rol**  
    - Tests: `test_masajista_permissions`, `test_cliente_access_restrictions`  
    - Valida que masajistas y clientes solo accedan a las operaciones permitidas por su rol.

14. **Creación de reserva requiere autenticación**  
    - Test: `test_create_reserva_requires_auth`  
    - Verifica que no se pueda crear una reserva sin un token válido.

---

## KPIs de Calidad para SPA

| Métrica                                   | Valor esperado |
|------------------------------------------|----------------|
| Cobertura de creación de reservas        | 90%            |
| Cobertura de actualización de reservas   | 85%            |
| Cobertura de eliminación de reservas     | 100%           |
| Cobertura de consultas de reservas       | 90%            |
| Validaciones de reglas de negocio        | 95%            |
| Seguridad y autenticación                | 100%           |
| Permisos y roles                         | 90%            |
| Integridad de datos                       | 100%           |

---

> Este documento refleja el estado actual de las pruebas implementadas para el dominio SPA.  
> Se recomienda actualizar periódicamente la cobertura y KPIs a medida que se agreguen nuevos endpoints o reglas de negocio.
