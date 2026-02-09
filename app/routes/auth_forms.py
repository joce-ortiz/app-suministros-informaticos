from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models.user_model import User


class RegistrationForm(FlaskForm):
    """
    Formulario para el registro de nuevos usuarios.
    """
    username = StringField('Nombre de Usuario',
                           validators=[DataRequired(), Length(min=4, max=80)])

    password = PasswordField('Contraseña',
                             validators=[DataRequired(), Length(min=6)])

    confirm_password = PasswordField('Confirmar Contraseña',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Registrarse')

    # --- Validación Personalizada ---
    def validate_username(self, username):
        """
        Verifica que el nombre de usuario no exista ya en la base de datos.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ese nombre de usuario ya existe. Por favor, elige otro.')


class LoginForm(FlaskForm):
    """
    Formulario para el inicio de sesión de usuarios.
    """
    username = StringField('Nombre de Usuario',
                           validators=[DataRequired()])

    password = PasswordField('Contraseña',
                             validators=[DataRequired()])

    remember = BooleanField('Recuérdame')

    submit = SubmitField('Iniciar Sesión')


class EditUserForm(FlaskForm):
    """
    Formulario para que el administrador edite usuarios.
    Permite cambiar nombre y rol.
    """
    username = StringField('Nombre de Usuario',
                           validators=[DataRequired(), Length(min=4, max=80)])

    role = SelectField('Rol del Usuario',
                       choices=[('cliente', 'Cliente'), ('admin', 'Administrador')],
                       validators=[DataRequired()])

    submit = SubmitField('Actualizar Usuario')