from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
import io
from xhtml2pdf import pisa
from flask import make_response
from datetime import datetime

# Importamos formularios y servicios
from app.routes.product_forms import ProductForm
from app.services import product_service, supplier_service

# Ya no importamos 'save_picture' ni 'db' porque no guardamos imágenes manuales

# Creamos el Blueprint
product_bp = Blueprint('product_routes', __name__)


# --- DECORADOR PERSONALIZADO ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('No tienes permiso para acceder a esta página.', 'danger')
            return redirect(url_for('auth_routes.home'))
        return f(*args, **kwargs)

    return decorated_function


# --- RUTAS ---

@product_bp.route('/')
@login_required
def product_list():
    """
    Muestra la lista de productos.
    Incluye: Búsqueda y Alertas de Stock.
    """
    # 1. Lógica de Búsqueda
    search_query = request.args.get('q')

    if search_query:
        products = product_service.search_products(search_query)
        if not products:
            flash(f'No se encontraron productos para "{search_query}"', 'warning')
        else:
            flash(f'Mostrando resultados para: "{search_query}"', 'info')
    else:
        products = product_service.get_all_products()

    # 2. Lógica de Alertas
    stock_alerts = product_service.get_stock_alerts()

    return render_template('product_list.html',
                           title='Inventario de Productos',
                           products=products,
                           alerts=stock_alerts,
                           current_query=search_query)


@product_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def create_product():
    """
    Crea un nuevo producto.
    Incluye: Selección de Proveedores.
    """
    form = ProductForm()

    # Rellenar las opciones del select múltiple
    all_suppliers = supplier_service.get_all_suppliers()
    form.suppliers.choices = [(s.id, s.nombre_empresa) for s in all_suppliers]

    if form.validate_on_submit():
        # Crear el producto (el servicio maneja los datos del form)
        new_product = product_service.create_product(form.data)

        if new_product:
            flash(f'Producto "{new_product.nombre}" creado exitosamente.', 'success')
            return redirect(url_for('product_routes.product_list'))
        else:
            flash('Error al crear el producto.', 'danger')

    return render_template('product_form.html',
                           title='Nuevo Producto',
                           form=form,
                           form_action=url_for('product_routes.create_product'))


@product_bp.route('/<int:product_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def update_product(product_id):
    """
    Edita un producto existente.
    Incluye: Precarga de proveedores.
    """
    product = product_service.get_product_by_id(product_id)
    if not product:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('product_routes.product_list'))

    # Cargamos el formulario con los datos del objeto
    form = ProductForm(obj=product)

    # Rellenar opciones de proveedores
    all_suppliers = supplier_service.get_all_suppliers()
    form.suppliers.choices = [(s.id, s.nombre_empresa) for s in all_suppliers]

    # Si es GET, marcamos los proveedores que ya tiene asignados
    if request.method == 'GET':
        form.suppliers.data = [s.id for s in product.suppliers]

    if form.validate_on_submit():
        # Actualizar datos y proveedores
        updated_product = product_service.update_product(product, form.data)

        if updated_product:
            flash(f'Producto "{updated_product.nombre}" actualizado.', 'success')
            return redirect(url_for('product_routes.product_list'))
        else:
            flash('Error al actualizar el producto.', 'danger')

    return render_template('product_form.html',
                           title='Editar Producto',
                           form=form,
                           form_action=url_for('product_routes.update_product', product_id=product_id))


@product_bp.route('/<int:product_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    """
    Elimina un producto.
    """
    success = product_service.delete_product(product_id)

    if success:
        flash('Producto eliminado exitosamente.', 'success')
    else:
        flash('Error al eliminar el producto.', 'danger')

    return redirect(url_for('product_routes.product_list'))


@product_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """
    Panel de Estadísticas (Gráficas).
    """
    stats = product_service.get_inventory_statistics()

    return render_template('dashboard.html',
                           title='Dashboard Administrativo',
                           names=stats['names'],
                           current_stock=stats['current_stock'],
                           target_stock=stats['target_stock'])


@product_bp.route('/reporte_pdf')
@login_required
def generate_pdf():
    """
    Genera un PDF con el listado actual de productos.
    """
    # 1. Obtener datos
    products = product_service.get_all_products()
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    # 2. Renderizar la plantilla HTML a un string
    rendered_html = render_template('report_pdf.html', products=products, fecha_actual=fecha)

    # 3. Crear el PDF usando xhtml2pdf
    pdf_output = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(rendered_html.encode('utf-8')), dest=pdf_output)

    # 4. Verificar errores
    if pisa_status.err:
        flash('Hubo un error al generar el PDF', 'danger')
        return redirect(url_for('product_routes.product_list'))

    # 5. Preparar la respuesta para descargar
    pdf_output.seek(0)
    response = make_response(pdf_output.read())
    response.headers['Content-Type'] = 'application/pdf'
    # 'attachment' hace que se descargue. 'inline' haría que se abra en el navegador.
    response.headers['Content-Disposition'] = 'attachment; filename=inventario.pdf'

    return response