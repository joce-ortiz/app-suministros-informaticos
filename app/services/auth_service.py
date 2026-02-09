from app import db, bcrypt
from app.models.user_model import User
from flask_login import login_user, logout_user


def register_user(username, password):
    """
    Lógica de negocio para registrar un nuevo usuario.
    Hashea la contraseña y guarda el usuario en la BD.
    """
    try:
        # El hasheo de la contraseña se hace automáticamente
        # gracias al @password.setter que definimos en el modelo.
        new_user = User(username=username, password=password)

        # Asignamos rol 'admin' al primer usuario que se registre
        if User.query.count() == 0:
            new_user.role = 'admin'

        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()  # Deshacer cambios si algo falla
        print(f"Error al registrar usuario: {e}")  # Mejor usar logging en producción
        return None


def attempt_login(username, password):
    """
    Lógica de negocio para intentar un inicio de sesión.
    """
    try:
        # 1. Encontrar al usuario
        user = User.query.filter_by(username=username).first()

        # 2. Verificar si el usuario existe Y si la contraseña es correcta
        if user and user.check_password(password):
            # 3. Registrar la sesión del usuario
            login_user(user)  # 'remember' se puede añadir aquí si se desea
            return user

        # Si el usuario no existe o la contraseña es incorrecta
        return None
    except Exception as e:
        print(f"Error al intentar login: {e}")
        return None


def logout_current_user():
    """
    Lógica de negocio para cerrar la sesión.
    """
    logout_user()

def get_all_users():
    """
    Devuelve una lista con todos los usuarios registrados.
    """
    try:
        return User.query.all()
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []

def change_user_role(user_id, new_role):
    """
    Cambia el rol de un usuario específico.
    """
    try:
        user = User.query.get(user_id)
        if user:
            user.role = new_role
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Error al cambiar rol: {e}")
        return False

def get_user_by_id(user_id):
    """
    Busca un usuario por su ID.
    """
    return User.query.get(user_id)

def update_user_details(user_id, new_username, new_role):
    """
    Actualiza los datos de un usuario (nombre y rol).
    """
    try:
        user = User.query.get(user_id)
        if user:
            user.username = new_username
            user.role = new_role
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Error al actualizar usuario: {e}")
        return False