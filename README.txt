FAPP
====

Configuración del entorno
-------------------------

1. Instala Python 3 si aún no lo tienes.
2. Crea un entorno virtual y actívalo:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Instala las dependencias del proyecto:

   ```bash
   pip install -r requirements.txt
   ```


Variables de entorno
--------------------

Antes de ejecutar el proyecto, define las siguientes variables de entorno:

```bash
export SECRET_KEY='tu-clave-secreta'
export DEBUG='False'  # o 'True' en desarrollo
export ALLOWED_HOSTS='localhost,127.0.0.1'
```

Si no defines `SECRET_KEY`, el proyecto utilizará un valor por defecto
válido solo para entornos de desarrollo. **En producción debes establecer
siempre esta variable.**


Dependencias
------------

El archivo `requirements.txt` incluye:

- Django: framework de desarrollo web.
- psycopg2-binary: adaptador de PostgreSQL para Python.
- xhtml2pdf: conversión de HTML a PDF.
- reportlab: generación de documentos PDF.
- django-adminlte3: integración del tema AdminLTE.
- django-bootstrap5: componentes de Bootstrap 5 para Django.
- Pillow: procesamiento de imágenes.

Base de datos
-------------

1. Asegúrate de tener un servidor de PostgreSQL en funcionamiento.
2. Crea la base de datos y el usuario con las credenciales definidas en `fapp/settings.py`:

   ```sql
   CREATE DATABASE fappdb;
   CREATE USER fappuser WITH PASSWORD 'fapppass';
   GRANT ALL PRIVILEGES ON DATABASE fappdb TO fappuser;
   ```

3. Configura las variables de entorno para la conexión:

   ```bash
    export POSTGRES_DB=fappdb
    export POSTGRES_USER=fappuser
    export POSTGRES_PASSWORD=fapppass
    export POSTGRES_HOST=localhost
    export POSTGRES_PORT=5432
```

Configuración en nuevos entornos
-------------------------------

Al iniciar la aplicación se verifica que las librerías externas
`xhtml2pdf` y `reportlab` estén instaladas y que la conexión con la base
de datos sea posible. Si falta alguna de estas dependencias o las
variables de entorno `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`,
`POSTGRES_HOST` o `POSTGRES_PORT`, se mostrará un mensaje de error
descriptivo para facilitar la configuración del entorno.

Migraciones y servidor
----------------------

1. Aplica las migraciones:

   ```bash
   python manage.py migrate
   ```
2. (Opcional) Crea un superusuario para acceder al panel de administración:

   ```bash
   python manage.py createsuperuser
   ```
3. Arranca el servidor de desarrollo:

   ```bash
   python manage.py runserver
   ```

Cargar datos de ejemplo
-----------------------

Puedes cargar datos de ejemplo utilizando fixtures de Django.
Coloca un archivo JSON con los datos en una carpeta `fixtures/` y ejecuta:

```bash
python manage.py loaddata datos_ejemplo.json
```

Esto poblará la base de datos con la información definida en el archivo.

