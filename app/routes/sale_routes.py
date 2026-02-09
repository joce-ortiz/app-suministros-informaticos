from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services import sale_service, product_service

sale_bp = Blueprint('sale_routes', __name__)


@sale_bp.route('/comprar/<int:product_id>', methods=['POST'])
@login_required
def buy_product(product_id):
    """
    Ruta para procesar la compra. Recibe la cantidad desde un formulario.
    """
    # Obtenemos la cantidad del formulario HTML (por defecto 1)
    try:
        cantidad = int(request.form.get('cantidad', 1))
    except ValueError:
        cantidad = 1

    if cantidad < 1:
        flash('La cantidad debe ser al menos 1.', 'danger')
        return redirect(url_for('product_routes.product_list'))

    # Llamamos al servicio
    success, message = sale_service.process_sale(current_user.id, product_id, cantidad)

    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('product_routes.product_list'))


@sale_bp.route('/mis-compras')
@login_required
def my_sales():
    """
    Muestra el historial de compras del usuario.
    """
    sales = sale_service.get_sales_by_user(current_user.id)
    return render_template('my_sales.html', title='Mis Compras', sales=sales)