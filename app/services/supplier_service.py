from app import db
from app.models.supplier_model import Supplier


def get_all_suppliers():
    """
    Obtiene todos los proveedores, ordenados por nombre.
    """
    try:
        return Supplier.query.order_by(Supplier.nombre_empresa).all()
    except Exception as e:
        print(f"Error al obtener proveedores: {e}")
        return []


def get_supplier_by_id(supplier_id):
    """
    Obtiene un proveedor específico por su ID.
    """
    try:
        return Supplier.query.get(supplier_id)
    except Exception as e:
        print(f"Error al obtener proveedor por ID: {e}")
        return None


def create_supplier(form_data):
    """
    Lógica de negocio para crear un nuevo proveedor.
    """
    try:
        new_supplier = Supplier(
            nombre_empresa=form_data['nombre_empresa'],
            telefono=form_data.get('telefono'),
            direccion=form_data.get('direccion'),
            cif=form_data.get('cif'),
            facturacion_info=form_data.get('facturacion_info'),
            descuento_porcentaje=form_data.get('descuento_porcentaje', 0.0),
            iva=form_data.get('iva', 21.0)
        )

        db.session.add(new_supplier)
        db.session.commit()
        return new_supplier
    except Exception as e:
        db.session.rollback()
        print(f"Error al crear proveedor: {e}")
        return None


def update_supplier(supplier, form_data):
    """
    Lógica de negocio para actualizar un proveedor existente.
    """
    try:
        supplier.nombre_empresa = form_data['nombre_empresa']
        supplier.telefono = form_data.get('telefono')
        supplier.direccion = form_data.get('direccion')
        supplier.cif = form_data.get('cif')
        supplier.facturacion_info = form_data.get('facturacion_info')
        supplier.descuento_porcentaje = form_data.get('descuento_porcentaje', 0.0)
        supplier.iva = form_data.get('iva', 21.0)

        db.session.commit()
        return supplier
    except Exception as e:
        db.session.rollback()
        print(f"Error al actualizar proveedor: {e}")
        return None


def delete_supplier(supplier_id):
    """
    Lógica de negocio para eliminar un proveedor.
    """
    try:
        supplier = Supplier.query.get(supplier_id)
        if supplier:
            # ¡Importante! Antes de eliminar, desasociar productos
            # (Si no, la BD podría dar error de clave foránea)
            supplier.products.clear()
            db.session.commit()

            db.session.delete(supplier)
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar proveedor: {e}")
        return False