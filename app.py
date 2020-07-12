# app.py

"""Main app"""

# Retic
from retic import App as app

# Routes
from routes.routes import router

# Definir la ruta del archivo de variables de entorno
app.env.read_env('.env')

# Agregar las rutas a la aplicación
app.use(router)

# Crear un servidor web
app.listen(
    use_reloader=True,
    use_debugger=True,
    hostname=app.env('APP_HOSTNAME', "localhost"),
    port=app.env.int('APP_PORT', 1801),
)
