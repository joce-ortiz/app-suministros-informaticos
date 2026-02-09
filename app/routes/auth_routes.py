from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app.routes.auth_forms import LoginForm, RegistrationForm, EditUserForm
from app.services import auth_service
from app.routes.product_routes import admin_required

# Creamos el "Blueprint" para estas rutas de autenticación
auth_bp = Blueprint('auth_routes', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Ruta para la página de registro de usuarios.
    """
    # Si el usuario ya está logueado, redirigir al inicio
    if current_user.is_authenticated:
        return redirect(url_for('auth_routes.home'))  # Cambiaremos 'home' luego

    form = RegistrationForm()

    # Si el formulario es enviado (POST) y es válido
    if form.validate_on_submit():
        # 1. Llamar a la Capa de Servicio
        user = auth_service.register_user(
            username=form.username.data,
            password=form.password.data
        )

        if user:
            # 2. Mostrar mensaje de éxito y redirigir
            flash('¡Tu cuenta ha sido creada! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth_routes.login'))
        else:
            flash('Hubo un error durante el registro.', 'danger')

    # Si es GET o el formulario no es válido, mostrar la página de registro
    return render_template('register.html', title='Registro', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Ruta para la página de inicio de sesión.
    """
    if current_user.is_authenticated:
        return redirect(url_for('auth_routes.home'))  # Cambiaremos 'home' luego

    form = LoginForm()

    if form.validate_on_submit():
        # 1. Llamar a la Capa de Servicio
        user = auth_service.attempt_login(
            username=form.username.data,
            password=form.password.data
        )

        if user:
            # 2. Si el login es exitoso, redirigir (Flask-Login ya hizo su trabajo)
            flash('Inicio de sesión exitoso.', 'success')
            # 'next' es una página a la que el usuario intentaba ir antes de loguearse
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('auth_routes.home'))
        else:
            # 3. Si falla, mostrar error
            flash('Inicio de sesión fallido. Revisa tu usuario y contraseña.', 'danger')

    return render_template('login.html', title='Iniciar Sesión', form=form)


@auth_bp.route('/logout')
@login_required  # Proteger esta ruta: solo usuarios logueados pueden verla
def logout():
    """
    Ruta para cerrar sesión.
    """
    auth_service.logout_current_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth_routes.login'))


@auth_bp.route('/')
@auth_bp.route('/home')
@login_required  # Proteger la página de inicio
def home():
    """
    Página de inicio (temporal).
    """
    return render_template('home.html', title='Inicio')


@auth_bp.route('/usuarios')
@login_required
@admin_required  # ¡Solo el admin puede ver esto!
def user_list():
    """
    Muestra una lista de todos los usuarios para gestionarlos.
    """
    users = auth_service.get_all_users()
    return render_template('user_list.html', title='Gestión de Usuarios', users=users)


@auth_bp.route('/usuarios/cambiar-rol/<int:user_id>/<new_role>', methods=['POST'])
@login_required
@admin_required
def change_role(user_id, new_role):
    """
    Cambia el rol de un usuario y redirige a la lista.
    """
    # Protección: Evitar que un admin se quite permisos a sí mismo por error
    if user_id == current_user.id and new_role != 'admin':
        flash('No puedes quitarte permisos de administrador a ti mismo.', 'warning')
        return redirect(url_for('auth_routes.user_list'))

    success = auth_service.change_user_role(user_id, new_role)

    if success:
        flash(f'Rol actualizado a "{new_role}" correctamente.', 'success')
    else:
        flash('Error al actualizar el rol.', 'danger')

    return redirect(url_for('auth_routes.user_list'))


@auth_bp.route('/usuarios/<int:user_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required  # ¡Solo admin!
def edit_user(user_id):
    """
    Ruta para editar nombre y rol de un usuario.
    """
    user = auth_service.get_user_by_id(user_id)
    if not user:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('auth_routes.user_list'))

    # Preparamos el formulario con los datos actuales del usuario
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        # Protección: No permitir que un admin se quite su propio rol de admin
        if user.id == current_user.id and form.role.data != 'admin':
            flash('No puedes quitarte permisos de administrador a ti mismo.', 'warning')
            # Recargamos la página para deshacer el cambio visual en el form
            return redirect(url_for('auth_routes.edit_user', user_id=user.id))

        success = auth_service.update_user_details(
            user_id=user.id,
            new_username=form.username.data,
            new_role=form.role.data
        )

        if success:
            flash(f'Usuario "{form.username.data}" actualizado correctamente.', 'success')
            return redirect(url_for('auth_routes.user_list'))
        else:
            flash('Error al actualizar el usuario. Puede que el nombre ya exista.', 'danger')

    return render_template('edit_user.html', title='Editar Usuario', form=form, user=user)