# Guía de Contribución - Django Dev Pro

¡Gracias por tu interés en contribuir a Django Dev Pro! Este documento te guiará en cómo hacerlo.

## 🤝 Cómo Contribuir

### 1. Fork el Repositorio

```bash
# Haz un fork en GitHub
# Luego clona tu fork
git clone https://github.com/djcrespo/django-skill.git
cd django-skill
```

### 2. Crea una Rama

```bash
# Crea una rama descriptiva
git checkout -b feature/descripcion-caracteristica
# o
git checkout -b bugfix/descripcion-del-bug
```

### 3. Realiza Cambios

Asegúrate de:
- ✅ Seguir el estilo de código existente
- ✅ Agregar tests para nuevas funcionalidades
- ✅ Actualizar documentación
- ✅ Mantener compatibilidad con Python 3.10+

### 4. Commit y Push

```bash
git add .
git commit -m "descripción clara del cambio"
git push origin tu-rama
```

### 5. Pull Request

- Abre un PR describiendo los cambios
- Referencia cualquier issue relacionado
- Espera revisión y feedback

## 📋 Estándares de Código

### Python

```python
# ✅ Bien: Docstrings en Google format
def detect_current_project(self) -> Optional[Dict]:
    """
    Detecta si el directorio actual es un proyecto Django.
    
    Returns:
        Dict con información del proyecto o None
    """
    pass

# ✅ Bien: Type hints
def generate_model(self, model_name: str, fields: List[Dict]) -> str:
    pass

# ✅ Bien: Nombres descriptivos
project_detector = ProjectDetector()
model_code = generator.generate_model(model_name, fields)

# ❌ Evitar: Variables ambiguas
d = ProjectDetector()
code = generator.generate_model(m, f)
```

### Estructura de Archivos

```
lib/
├── core/              # Módulos core (detectores, analizadores)
├── generators/        # Generadores de código
├── executors/         # Ejecutores de comandos
├── config/            # Gestión de configuración
├── workflow/          # Flujos de trabajo
└── utils/             # Utilidades
```

## 🧪 Testing

```bash
# Ejecuta los tests
python3 -m pytest

# Con cobertura
python3 -m pytest --cov=lib
```

## 📚 Documentación

- Actualiza README.md si cambias funcionalidad
- Agrega ejemplos en examples/usage_examples.md
- Documenta nuevos módulos en docstrings

## 🐛 Reportar Bugs

Crea un issue con:
- Descripción clara del problema
- Pasos para reproducir
- Versión de Python
- Sistema operativo
- Logs/errores relevantes

## 💡 Sugerir Características

Crea un issue con:
- Descripción de la característica
- Caso de uso
- Ejemplos de cómo debería funcionar

## 📝 Commit Messages

Usa el patrón:

```
tipo: descripción corta

descripción más detallada si es necesario

fixes #123
```

**Tipos válidos:**
- `feat`: Nueva característica
- `fix`: Corrección de bug
- `docs`: Cambios de documentación
- `refactor`: Refactorización de código
- `test`: Agregación o actualización de tests
- `chore`: Cambios de configuración

## 🔄 Proceso de Revisión

1. Un mantenedor revisará tu PR
2. Pueden solicitar cambios
3. Una vez aprobado, se mergea
4. Se agrega a la siguiente versión

## 📦 Release Process

Los mantenedores seguirán:
1. Bump version en skill.yml
2. Update CHANGELOG.md
3. Tag en git
4. Push a PyPI (si aplica)

## ❓ Preguntas?

- Lee la documentación: README.md, INSTALLATION.md
- Abre un issue con tag `question`
- Contacta a los mantenedores

## ✨ Gracias por Contribuir!

Tu contribución ayuda a que Django Dev Pro sea mejor para todos.
