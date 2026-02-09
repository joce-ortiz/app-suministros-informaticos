from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange
from app.models.supplier_model import Supplier


class SupplierForm(FlaskForm):
    """
    Formulario para crear o editar un Proveedor.
    """
    nombre_empresa = StringField('Nombre de la Empresa',
                                 validators=[DataRequired()])

    telefono = StringField('Teléfono')

    direccion = StringField('Dirección')

    cif = StringField('CIF/NIF')

    facturacion_info = TextAreaField('Información de Facturación')

    descuento_porcentaje = FloatField('Descuento (%)',
                                      validators=[Optional(), NumberRange(min=0, max=100)],
                                      default=0.0)

    iva = FloatField('IVA (%)',
                     validators=[Optional(), NumberRange(min=0, max=100)],
                     default=21.0)

    submit = SubmitField('Guardar Proveedor')