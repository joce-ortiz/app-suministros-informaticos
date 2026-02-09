from app import db
from datetime import datetime


class Sale(db.Model):
    """
    Modelo para registrar una venta.
    Conecta Usuario y Producto.
    """
    __tablename__ = 'sale'

    id = db.Column(db.Integer, primary_key=True)

    # Fecha de la compra (automática)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Cantidad comprada
    cantidad = db.Column(db.Integer, nullable=False)

    # Precio unitario AL MOMENTO de la compra (por si cambias precios en el futuro)
    precio_unitario = db.Column(db.Float, nullable=False)

    # Relaciones (Foreign Keys)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    # Relaciones para acceder a los objetos
    user = db.relationship('User', backref=db.backref('sales', lazy=True))
    product = db.relationship('Product', backref=db.backref('sales', lazy=True))

    @property
    def total(self):
        return self.cantidad * self.precio_unitario