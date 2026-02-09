from app import db
from app.models.product_model import Product
from app.models.supplier_model import Supplier
from sqlalchemy import or_

def get_all_products():
    """
    Obtiene todos los productos de la base de datos, ordenados por nombre.
    """
    try:
        return Product.query.order_by(Product.nombre).all()
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []


def get_product_by_id(product_id):
    """
    Obtiene un producto específico por su ID.
    """
    try:
        return Product.query.get(product_id)
    except Exception as e:
        print(f"Error al obtener producto por ID: {e}")
        return None


def create_product(form_data):
    """
    Lógica de negocio para crear un nuevo producto.
    """
    try:
        new_product = Product(
            nombre=form_data['nombre'],
            referencia=form_data.get('referencia'),
            descripcion=form_data.get('descripcion'),
            precio=form_data['precio'],
            cantidad_stock=form_data['cantidad_stock'],
            stock_objetivo=form_data['stock_objetivo'],
            ubicacion=form_data.get('ubicacion')
        )

        # --- LÓGICA PARA PROVEEDORES ---
        supplier_ids = form_data.get('suppliers', [])
        if supplier_ids:
            suppliers = Supplier.query.filter(Supplier.id.in_(supplier_ids)).all()
            new_product.suppliers.extend(suppliers)

        db.session.add(new_product)
        db.session.commit()
        return new_product
    except Exception as e:
        db.session.rollback()
        print(f"Error al crear producto: {e}")
        return None


def update_product(product, form_data):
    """
    Lógica de negocio para actualizar un producto existente.
    """
    try:
        product.nombre = form_data['nombre']
        product.referencia = form_data.get('referencia')
        product.descripcion = form_data.get('descripcion')
        product.precio = form_data['precio']
        product.cantidad_stock = form_data['cantidad_stock']
        product.stock_objetivo = form_data['stock_objetivo']
        product.ubicacion = form_data.get('ubicacion')

        # --- ACTUALIZAR PROVEEDORES ---
        supplier_ids = form_data.get('suppliers', [])
        product.suppliers.clear()
        if supplier_ids:
            suppliers = Supplier.query.filter(Supplier.id.in_(supplier_ids)).all()
            product.suppliers.extend(suppliers)

        db.session.commit()
        return product
    except Exception as e:
        db.session.rollback()
        print(f"Error al actualizar producto: {e}")
        return None


def delete_product(product_id):
    """
    Lógica de negocio para eliminar un producto.
    """
    try:
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar producto: {e}")
        return False


def get_stock_alerts():
    """
    Obtiene todos los productos que están por debajo de su umbral de stock (10%).
    """
    try:
        products = Product.query.all()
        alerts = [product for product in products if product.stock_alert]
        return alerts
    except Exception as e:
        print(f"Error al obtener alertas de stock: {e}")
        return []

def get_inventory_statistics():
    """
    Prepara los datos para las gráficas del Dashboard.
    Devuelve tres listas: Nombres, Stock Actual, Stock Objetivo.
     """
    try:
        products = Product.query.all()

        # Creamos listas vacías
        names = []
        current_stock = []
        target_stock = []

        for product in products:
            names.append(product.nombre)
            current_stock.append(product.cantidad_stock)
            target_stock.append(product.stock_objetivo)

        return {
            'names': names,
            'current_stock': current_stock,
            'target_stock': target_stock
        }
    except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {'names': [], 'current_stock': [], 'target_stock': []}


def search_products(query):
    """
    Busca productos cuyo nombre O referencia contengan el texto 'query'.
    Usa ilike para que no importen las mayúsculas/minúsculas.
    """
    try:
        search_term = f"%{query}%"  # Los % son comodines en SQL

        return Product.query.filter(
            or_(
                Product.nombre.ilike(search_term),
                Product.referencia.ilike(search_term)
            )
        ).order_by(Product.nombre).all()
    except Exception as e:
        print(f"Error en la búsqueda: {e}")
        return []