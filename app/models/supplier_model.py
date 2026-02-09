from app import db

# Importamos la tabla de asociación que definiremos en product_model
# Usamos un 'try-except' para evitar un error de importación circular
# durante la inicialización de la app.
try:
    from app.models.product_model import product_supplier_association
except ImportError:
    pass


class Supplier(db.Model):
    """
    Modelo de Base de Datos para un Proveedor.
    Cumple el requisito 3.9.
    """
    __tablename__ = 'supplier'

    id = db.Column(db.Integer, primary_key=True)

    # Datos de contacto
    nombre_empresa = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    cif = db.Column(db.String(20), unique=True)

    # Datos de facturación
    facturacion_info = db.Column(db.Text)
    descuento_porcentaje = db.Column(db.Float, default=0.0)
    iva = db.Column(db.Float, default=21.0)  # Asumimos un IVA por defecto

    # --- Relación Muchos-a-Muchas ---
    # 'products' es un campo "virtual" que nos dará una lista de
    # objetos Producto asociados a este Proveedor.
    products = db.relationship(
        'Product',
        secondary='product_supplier_association',  # Nombre de la tabla de asociación
        back_populates='suppliers'
    )

    def __repr__(self):
        return f'<Supplier {self.nombre_empresa}>'