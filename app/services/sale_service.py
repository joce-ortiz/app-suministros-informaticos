from app import db
from app.models.sale_model import Sale
from app.models.product_model import Product
from app.utils import send_stock_alert

def process_sale(user_id, product_id, cantidad):
    """
    Procesa una venta:
    1. Verifica stock.
    2. Crea el registro de venta.
    3. Resta el stock del producto.
    """
    try:
        product = Product.query.get(product_id)

        if not product:
            return False, "Producto no encontrado."

        if product.cantidad_stock < cantidad:
            return False, f"No hay suficiente stock. Quedan {product.cantidad_stock} unidades."

        # Creamos la venta
        new_sale = Sale(
            user_id=user_id,
            product_id=product_id,
            cantidad=cantidad,
            precio_unitario=product.precio
        )

        # RESTAMOS EL STOCK
        product.cantidad_stock -= cantidad

        db.session.add(new_sale)
        db.session.commit()

        # --- 2. VERIFICAR ALERTA DE STOCK ---
        # Usamos la propiedad .stock_alert que definimos en el Modelo Product
        if product.stock_alert:
            # Enviamos el correo (esto puede tardar un par de segundos)
            send_stock_alert(product)

        return True, "¡Compra realizada con éxito!"

    except Exception as e:
        db.session.rollback()
        print(f"Error en venta: {e}")
        return False, "Error interno al procesar la venta."


def get_sales_by_user(user_id):
    """Obtiene el historial de compras de un usuario."""
    return Sale.query.filter_by(user_id=user_id).order_by(Sale.fecha.desc()).all()


def get_all_sales():
    """Obtiene todas las ventas (para admin)."""
    return Sale.query.order_by(Sale.fecha.desc()).all()