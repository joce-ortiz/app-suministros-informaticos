from app import db

# --- Tabla de Asociación ---
product_supplier_association = db.Table('product_supplier_association',
                                        db.Column('product_id', db.Integer, db.ForeignKey('product.id'),
                                                  primary_key=True),
                                        db.Column('supplier_id', db.Integer, db.ForeignKey('supplier.id'),
                                                  primary_key=True)
                                        )

class Product(db.Model):
    """
    Modelo de Base de Datos para un Producto.
    """
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)

    # Datos del producto
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    nombre = db.Column(db.String(100), nullable=False)
    referencia = db.Column(db.String(50), unique=True)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    ubicacion = db.Column(db.String(100))

    # Gestión de inventario
    cantidad_stock = db.Column(db.Integer, nullable=False, default=0)

    # Interpretación del requisito ("al 90%"):
    # Asumimos que es 90% *consumido* (o sea, queda el 10%).
    # Definimos un 'stock_objetivo' (100%) y la alerta salta
    # si el stock actual es <= 10% de ese objetivo.
    stock_objetivo = db.Column(db.Integer, nullable=False, default=100)

    # --- Relación Muchos-a-Muchas ---
    # 'suppliers' es un campo "virtual" que nos dará una lista de
    # objetos Supplier asociados a este Producto.
    suppliers = db.relationship(
        'Supplier',
        secondary=product_supplier_association,
        back_populates='products'
    )

    # --- Propiedad para la Alerta de Stock ---
    @property
    def stock_alert(self):
        """
        Propiedad que devuelve True si el stock es peligrosamente bajo.
        """
        if self.stock_objetivo == 0:
            return False  # Evitar división por cero

        # Calcula el 10% del stock objetivo (el 90% consumido)
        umbral_minimo = self.stock_objetivo * 0.10
        return self.cantidad_stock <= umbral_minimo

    def __repr__(self):
        return f'<Product {self.nombre} (Ref: {self.referencia})>'