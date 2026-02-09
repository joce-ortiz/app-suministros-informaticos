from flask_mail import Message
from app import mail


def send_stock_alert(product):
    """
    Envía un correo electrónico al administrador avisando del stock bajo.
    Se llama automáticamente desde 'sale_service.py' cuando una venta
    deja el stock por debajo del umbral mínimo (10%).
    """
    try:
        # Configuración del mensaje
        msg = Message(
            subject=f'⚠️ Alerta de Stock: {product.nombre}',
            sender='noreply@tutienda.com',  # Quién envía el correo (visual)
            recipients=['admin@tutienda.com']  # A quién le llega (PON TU CORREO REAL AQUÍ SI QUIERES PROBARLO)
        )

        # Cuerpo del mensaje
        msg.body = f"""
        Hola Administrador,

        El sistema de gestión ha detectado que un producto ha alcanzado niveles críticos de inventario:

        ----------------------------------------
        Producto:       {product.nombre}
        Referencia:     {product.referencia if product.referencia else 'N/A'}
        Stock Actual:   {product.cantidad_stock} unidades
        Stock Objetivo: {product.stock_objetivo} unidades
        ----------------------------------------

        Por favor, contacta a los proveedores para realizar un reabastecimiento.

        Atentamente,
        Tu App de Suministros Informáticos
        """

        # Enviar el correo usando la instancia 'mail' configurada en __init__.py
        mail.send(msg)
        print(f"Correo de alerta enviado exitosamente para el producto: {product.nombre}")

    except Exception as e:
        # Imprimimos el error en la consola para no detener la aplicación si el correo falla
        print(f"Error al enviar correo de alerta: {e}")