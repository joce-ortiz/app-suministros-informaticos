from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.routes.supplier_forms import SupplierForm
from app.services import supplier_service
from app.routes.product_routes import admin_required

# Creamos el Blueprint para proveedores
supplier_bp = Blueprint('supplier_routes', __name__)


@supplier_bp.route('/')
@login_required
def supplier_list():
    """
    Ruta para LEER (Read) - Muestra la lista de todos los proveedores.
    """
    suppliers = supplier_service.get_all_suppliers()
    return render_template('supplier_list.html',
                           title='Proveedores',
                           suppliers=suppliers)


@supplier_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def create_supplier():
    """
    Ruta para CREAR (Create) - Formulario para nuevo proveedor.
    """
    form = SupplierForm()

    if form.validate_on_submit():
        new_supplier = supplier_service.create_supplier(form.data)
        if new_supplier:
            flash(f'Proveedor "{new_supplier.nombre_empresa}" creado.', 'success')
            return redirect(url_for('supplier_routes.supplier_list'))
        else:
            flash('Error al crear el proveedor.', 'danger')

    return render_template('supplier_form.html',
                           title='Nuevo Proveedor',
                           form=form,
                           form_action=url_for('supplier_routes.create_supplier'))


@supplier_bp.route('/<int:supplier_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def update_supplier(supplier_id):
    """
    Ruta para ACTUALIZAR (Update) - Formulario para editar proveedor.
    """
    supplier = supplier_service.get_supplier_by_id(supplier_id)
    if not supplier:
        flash('Proveedor no encontrado.', 'danger')
        return redirect(url_for('supplier_routes.supplier_list'))

    form = SupplierForm(obj=supplier)

    if form.validate_on_submit():
        updated_supplier = supplier_service.update_supplier(supplier, form.data)
        if updated_supplier:
            flash(f'Proveedor "{updated_supplier.nombre_empresa}" actualizado.', 'success')
            return redirect(url_for('supplier_routes.supplier_list'))
        else:
            flash('Error al actualizar el proveedor.', 'danger')

    return render_template('supplier_form.html',
                           title='Editar Proveedor',
                           form=form,
                           form_action=url_for('supplier_routes.update_supplier', supplier_id=supplier_id))


@supplier_bp.route('/<int:supplier_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def delete_supplier(supplier_id):
    """
    Ruta para ELIMINAR (Delete) - Elimina un proveedor.
    """
    success = supplier_service.delete_supplier(supplier_id)
    if success:
        flash('Proveedor eliminado exitosamente.', 'success')
    else:
        flash('Error al eliminar el proveedor.', 'danger')

    return redirect(url_for('supplier_routes.supplier_list'))