# Importamos la función 'create_app' que escribiremos en app/__init__.py
from app import create_app

# Creamos la instancia de la aplicación
app = create_app()

# Esta línea permite ejecutar la app con 'python run.py'
if __name__ == '__main__':
    app.run(debug=True)