from app import db, login_manager, bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """
    Función requerida por Flask-Login.
    Permite cargar el usuario actual desde la sesión.
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    Modelo de Base de Datos para un Usuario.
    Hereda de db.Model (para SQLAlchemy) y UserMixin (para Flask-Login).
    """

    # Nombre de la tabla en la base de datos
    __tablename__ = 'user'

    # --- Columnas de la Tabla ---

    # Llave primaria
    id = db.Column(db.Integer, primary_key=True)

    # Nombre de usuario. Debe ser único y no puede ser nulo.
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Hash de la contraseña. No guardamos la contraseña en texto plano.
    password_hash = db.Column(db.String(128), nullable=False)

    # Rol del usuario ('admin' o 'cliente') para control de acceso.
    # Requisito 3.5: "dos tipos de acceso, uno para clientes y otro para nosotros"
    role = db.Column(db.String(20), nullable=False, default='cliente')

    # --- Métodos Útiles ---

    # Propiedad 'password' que no se puede leer, solo escribir (set).
    @property
    def password(self):
        raise AttributeError('¡El password no es un atributo legible!')

    # Método para "hashear" (encriptar) la contraseña al asignarla.
    @password.setter
    def password(self, password_texto_plano):
        self.password_hash = bcrypt.generate_password_hash(password_texto_plano).decode('utf-8')

    # Método para verificar la contraseña durante el login.
    def check_password(self, password_texto_plano):
        return bcrypt.check_password_hash(self.password_hash, password_texto_plano)

    def __repr__(self):
        # Representación en string del objeto, útil para debugging.
        return f'<User {self.username} ({self.role})>'