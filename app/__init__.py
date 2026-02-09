from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

# 1. Creación de las instancias de las extensiones (Globales)
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()

# 2. Configuración del LoginManager
# Define a qué ruta se redirige si el usuario no está logueado
login_manager.login_view = 'auth_routes.login'
login_manager.login_message_category = 'info'


def create_app():
    """
    Fábrica de Aplicaciones (Application Factory).
    Crea y configura la instancia de la aplicación Flask.
    """
    app = Flask(__name__)

    # --- 3. CONFIGURACIÓN GENERAL ---
    # Clave secreta para proteger formularios y sesiones
    app.config['SECRET_KEY'] = 'mi_clave_secreta_12345_cambiar_despues'

    # Configuración de la Base de Datos (SQLite)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proyecto.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- 4. CONFIGURACIÓN DEL SERVIDOR DE CORREO (Para Alertas) ---
    # RECUERDA: Cambia estos datos por los de tu servidor real (Gmail, Mailtrap, etc.)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'tu_correo@gmail.com'  # <--- PON TU CORREO
    app.config['MAIL_PASSWORD'] = 'tu_contraseña_de_aplicacion'  # <--- PON TU CLAVE

    # --- 5. INICIALIZACIÓN DE EXTENSIONES CON LA APP ---
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # --- 6. REGISTRO DE BLUEPRINTS (RUTAS) ---
    # Importamos aquí dentro para evitar referencias circulares

    # Autenticación y Usuarios
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/')

    # Gestión de Productos (Incluye Dashboard y Reportes PDF)
    from app.routes.product_routes import product_bp
    app.register_blueprint(product_bp, url_prefix='/productos')

    # Gestión de Proveedores
    from app.routes.supplier_routes import supplier_bp
    app.register_blueprint(supplier_bp, url_prefix='/proveedores')

    # Gestión de Ventas (Carrito de compra)
    from app.routes.sale_routes import sale_bp
    app.register_blueprint(sale_bp, url_prefix='/ventas')

    return app