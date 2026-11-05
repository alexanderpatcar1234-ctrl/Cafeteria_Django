# Sistema Web de Pedidos para Cafetería

Sistema web desarrollado con **Django** para gestionar productos, usuarios y pedidos de una cafetería.

El proyecto permite trabajar con autenticación de usuarios, productos con imágenes, categorías, control de stock, pedidos y administración mediante Django Admin.

---

## Tecnologías utilizadas

- Python
- Django
- SQLite
- HTML
- Bootstrap
- Pillow
- Git
- GitHub
- GitHub Actions

---

## Funcionalidades

Actualmente el sistema incluye:

- Inicio de sesión.
- Cierre de sesión.
- Control de acceso a vistas protegidas.
- Gestión de usuarios.
- Gestión de categorías.
- CRUD de productos.
- Productos con imágenes.
- Control de stock.
- Gestión de pedidos.
- Consulta de pedidos por usuario.
- Panel de administración.
- Control de versiones con Git y GitHub.
- Verificación automática mediante GitHub Actions.

---

## Estructura principal del proyecto

```text
cafeteria_django/
│
├── .github/
│   └── workflows/
│
├── config/
│
├── pedidos/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── static/
├── media/
│
├── db.sqlite3
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

La carpeta del entorno virtual:

```text
entorno/
```

no se almacena en GitHub y debe crearse nuevamente en cada computadora.

---

# Instalación en una nueva computadora

## 1. Clonar el repositorio

Abrir **Git Bash** en la carpeta donde se almacenará el proyecto.

```bash
git clone URL_DEL_REPOSITORIO
```

Ejemplo:

```bash
git clone https://github.com/USUARIO/cafeteria_django.git
```

---

## 2. Ingresar a la carpeta del proyecto

```bash
cd cafeteria_django
```

Opcionalmente, abrir el proyecto directamente en Visual Studio Code:

```bash
code .
```

---

## 3. Crear el entorno virtual

Abrir una terminal **PowerShell** desde Visual Studio Code y ejecutar:

```powershell
python -m venv entorno
```

---

## 4. Habilitar temporalmente la ejecución de scripts

Ejecutar en PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Esta configuración solamente se aplica a la terminal actual.

---

## 5. Activar el entorno virtual

```powershell
.\entorno\Scripts\Activate.ps1
```

Si se activó correctamente, la terminal mostrará:

```text
(entorno)
```

al inicio de la línea.

---

## 6. Instalar las dependencias

```powershell
pip install -r requirements.txt
```

Esto instalará las bibliotecas necesarias para ejecutar el proyecto, como Django y Pillow.

---

## 7. Aplicar migraciones

```powershell
python manage.py migrate
```

Este comando aplica las migraciones que todavía se encuentren pendientes.

---

## 8. Comprobar la configuración de Django

```powershell
python manage.py check
```

Resultado esperado:

```text
System check identified no issues
```

---

## 9. Ejecutar el servidor

```powershell
python manage.py runserver
```

Django mostrará una dirección similar a:

```text
http://127.0.0.1:8000/
```

---

## 10. Abrir el sistema

Abrir en el navegador:

http://127.0.0.1:8000/

La página principal redirigirá automáticamente al inicio de sesión.

---

# Continuar el proyecto en una computadora donde ya fue clonado

Si el proyecto ya existe en la computadora, **no volver a ejecutar `git clone`**.

Abrir Git Bash dentro del proyecto y ejecutar:

```bash
git pull
```

Después abrir PowerShell y habilitar nuevamente la ejecución de scripts:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Activar el entorno:

```powershell
.\entorno\Scripts\Activate.ps1
```

Si las dependencias fueron modificadas:

```powershell
pip install -r requirements.txt
```

Aplicar posibles migraciones pendientes:

```powershell
python manage.py migrate
```

Finalmente:

```powershell
python manage.py runserver
```

---

# Guardar los avances en GitHub

Antes de finalizar cada sesión de laboratorio, abrir Git Bash dentro del proyecto.

## Revisar los cambios

```bash
git status
```

## Preparar los archivos

```bash
git add .
```

## Crear un commit

```bash
git commit -m "Actualizar avance del sistema"
```

## Publicar los cambios

```bash
git push
```

---

# Flujo de trabajo entre laboratorios

```text
INICIO DE LA SESIÓN
        ↓
git clone o git pull
        ↓
Crear / activar entorno
        ↓
Instalar requirements
        ↓
Aplicar migraciones
        ↓
Ejecutar proyecto
        ↓
DESARROLLO
        ↓
git add
        ↓
git commit
        ↓
git push
        ↓
FIN DE LA SESIÓN
```

---

# Archivos que se almacenan en GitHub

En este proyecto académico se almacenarán también:

```text
db.sqlite3
media/
```

Esto permite conservar entre los diferentes laboratorios:

- Usuarios.
- Categorías.
- Productos.
- Imágenes.
- Pedidos.
- Datos de prueba.

---

# Archivos que no se almacenan en GitHub

El archivo `.gitignore` evita subir elementos locales como:

```text
entorno/
__pycache__/
*.pyc
.vscode/
.env
```

El entorno virtual debe reconstruirse utilizando:

```powershell
python -m venv entorno
```

y:

```powershell
pip install -r requirements.txt
```

---

# Accesos principales

Una vez iniciado el servidor:

```text
Página principal:
http://127.0.0.1:8000/

Inicio de sesión:
http://127.0.0.1:8000/login/

Inicio del sistema:
http://127.0.0.1:8000/inicio/

Tienda:
http://127.0.0.1:8000/tienda/

Mis pedidos:
http://127.0.0.1:8000/mis-pedidos/

Administración:
http://127.0.0.1:8000/admin/
```

Las vistas del sistema requieren autenticación.

El acceso a Administración solamente está disponible para usuarios autorizados.

---

# GitHub Actions

Cada vez que se realiza un:

```bash
git push
```

GitHub Actions ejecuta automáticamente comprobaciones sobre el proyecto.

Entre ellas:

```text
Instalar dependencias
        ↓
Verificar Django
        ↓
Comprobar migraciones
        ↓
Aplicar migraciones
        ↓
Resultado
```

El resultado puede revisarse desde:

```text
Repositorio de GitHub
→ Actions
```