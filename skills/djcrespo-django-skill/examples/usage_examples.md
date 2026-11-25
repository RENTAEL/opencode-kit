# Ejemplos de Uso - Django Dev Pro Skill

> Los ejemplos usan rutas genéricas. Reemplaza `/path/to/your/project` por la ruta real de tu proyecto Django.

---

## Ejemplo 1: Primera ejecución / Estado del proyecto

```bash
$ cd /path/to/your/project
$ python lib/main.py --status
```

Salida esperada:

```text
Project: myproject
Path: /path/to/your/project
Configured: yes
Test command: python manage.py test
Env file: .env
Load env before commands: false
Apps found: products, orders
```

La primera vez que se ejecuta el helper en un proyecto, crea una configuración por defecto en `~/.django-dev-pro/commands.json`. Edita ese archivo manualmente para activar `.env`, pyenv o comandos personalizados.

---

## Ejemplo 2: Ejecutar Tests

Prompt a OpenCode:

```
Ejecuta los tests del proyecto
```

El helper ejecuta:

```bash
python lib/main.py --test
```

Salida esperada (cuando los tests pasan):

```text
$ python manage.py test
--- stdout ---
Found 12 test(s).
Creating test database...
System check identified no issues.
........................
----------------------------------------------------------------------
Ran 12 tests in 0.452s

OK
```

---

## Ejemplo 3: Ejecutar Tests con Auto-Fix

Prompt a OpenCode:

```
Ejecuta los tests y corrige los errores
```

El helper ejecuta:

```bash
python lib/main.py --test --auto-fix
```

Salida esperada cuando el fallo se debe a un `__init__.py` faltante:

```text
$ python manage.py test
--- stderr ---
ModuleNotFoundError: No module named 'products'
--- exit code: 1 ---

🔧 Auto-fix enabled (simple): attempting common fixes...
  Created missing /path/to/your/project/apps/products/__init__.py

🚀 Re-running tests after auto-fix...
$ python manage.py test
--- stdout ---
........................
Ran 12 tests in 0.461s

OK
```

Si no puede aplicar una corrección obvia, el helper informa el error y pide intervención manual.

---

## Ejemplo 4: Generar un CRUD completo

Prompt a OpenCode:

```
Crea un CRUD para Product con name, description y price en la app products
```

El helper ejecuta:

```bash
python lib/main.py --generate-crud Product --app products --fields name:CharField description:TextField price:DecimalField
```

Salida esperada:

```text
  Generated /path/to/your/project/apps/products/models.py
  Generated /path/to/your/project/apps/products/serializers.py
  Generated /path/to/your/project/apps/products/views.py
  Generated /path/to/your/project/apps/products/tests.py
  Generated /path/to/your/project/apps/products/urls.py
  Updated /path/to/your/project/config/urls.py

✅ CRUD generated for Product in app 'products'
```

Si no puede detectar el archivo principal de URLs del proyecto, muestra las instrucciones manuales para agregar:

```python
path('products/', include('products.urls')),
```

Pasos siguientes recomendados:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py test
```

---

## Ejemplo 5: Agregar un campo a un modelo existente

Prompt a OpenCode:

```
Agrega un campo priority de tipo IntegerField con default 0 al modelo Task
```

El helper ejecuta:

```bash
python lib/main.py --add-field priority:IntegerField:0 --model Task --app tasks
```

Salida esperada:

```text
✅ Added field 'priority' to Task in /path/to/your/project/apps/tasks/models.py
  Updated WriteSerializer fields in /path/to/your/project/apps/tasks/serializers.py
  Added minimal test for 'priority' in /path/to/your/project/apps/tasks/tests.py
```

Si no encuentra el serializer o el test, continúa sin romper los archivos existentes.

---

## Ejemplo 6: Mostrar Estado del Proyecto

Prompt a OpenCode:

```
Muestra el estado del proyecto
```

Salida esperada:

```text
Project: myproject
Path: /path/to/your/project
Configured: yes
Test command: python manage.py test
Env file: .env.local
Load env before commands: true
pyenv env: myenv
Apps found: products, orders, users
```

---

## Ejemplo 7: Cambiar de Proyecto

```bash
$ cd /path/to/your/other-project
$ python lib/main.py --status
```

Salida esperada:

```text
Project: other-project
Path: /path/to/your/other-project
Configured: yes
Test command: python manage.py test
Env file: .env
Load env before commands: false
Apps found: catalog, cart
```

El helper detecta automáticamente el nuevo proyecto y carga su configuración desde `~/.django-dev-pro/commands.json`.

---

Estos ejemplos reflejan el comportamiento actual de `lib/main.py`. Funcionalidades futuras (análisis automático de patrones, generación de migraciones, coverage, etc.) se añadirán en versiones posteriores.
