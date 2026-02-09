from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange



class ProductForm(FlaskForm):
    """
    Formulario para crear o editar un Producto.
    (Versión sin imágenes)
    """
    nombre = StringField('Nombre del Producto', validators=[DataRequired()])
    referencia = StringField('Número de Referencia')
    descripcion = TextAreaField('Descripción')
    precio = FloatField('Precio (€)', validators=[DataRequired(), NumberRange(min=0.01)])
    cantidad_stock = IntegerField('Cantidad en Stock', validators=[DataRequired(), NumberRange(min=0)])
    stock_objetivo = IntegerField('Stock Objetivo', validators=[DataRequired(), NumberRange(min=1)])
    ubicacion = StringField('Ubicación en Almacén')

    # Coerce=int asegura que los valores seleccionados se traten como números (IDs)
    suppliers = SelectMultipleField('Proveedores', coerce=int)

    submit = SubmitField('Guardar Producto')