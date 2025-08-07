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
   pip install django psycopg2-binary
   ```

Base de datos
-------------

1. Asegúrate de tener un servidor de PostgreSQL en funcionamiento.
2. Crea la base de datos y el usuario con las credenciales definidas en `fapp/settings.py`:

   ```sql
   CREATE DATABASE fappdb;
   CREATE USER fappuser WITH PASSWORD 'fapppass';
   GRANT ALL PRIVILEGES ON DATABASE fappdb TO fappuser;
   ```

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

