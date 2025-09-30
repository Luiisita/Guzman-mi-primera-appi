# Guía de Contribución - Clínica Dental (Dominio Tipo A)

## Proceso de Desarrollo

1. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
2. Desarrollar siguiendo la guía y los tests
3. Ejecutar calidad local: `./scripts/quality.sh` o usar las tareas en VS Code
4. Tests: asegurar cobertura > 80%
5. Commit: usar Conventional Commits (ej: feat: agregar endpoint de citas)
6. Push: `git push origin feature/nueva-funcionalidad`
7. PR: crear Pull Request y asignar reviewers

## Estándares de Código

- **Formateo**: Black (line-length = 88)
- **Imports**: isort (perfil: black)
- **Linting**: flake8
- **Tipos**: mypy
- **Seguridad**: bandit
- **Tests**: pytest con coverage mínimo 80%
