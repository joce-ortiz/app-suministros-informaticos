# 💻 Aplicación de Gestión para Empresa de Suministros Informáticos

**Proyecto Final - Curso de Programación Python**

## 📖 Descripción General
Este proyecto consiste en el desarrollo de una aplicación web "Full Stack" para la gestión integral de una empresa de suministros informáticos. La solución nace de la necesidad de digitalizar y optimizar el control de inventario, la gestión de proveedores y el registro de ventas.

La plataforma permite a los administradores mantener un control estricto sobre el stock, recibir alertas automáticas y analizar el rendimiento del negocio, mientras ofrece una interfaz para que los clientes consulten el catálogo y realicen pedidos.

## 🚀 Objetivos y Funcionalidades Clave

* **📦 Digitalización del Inventario:** Operaciones CRUD (Crear, Leer, Actualizar, Borrar) completas sobre productos y proveedores.
* **⚠️ Automatización de Alertas:** Sistema proactivo que notifica vía correo electrónico (SMTP) cuando el stock de un producto desciende del **10%** de su objetivo.
* **🔐 Seguridad y Roles:** Sistema de autenticación con roles diferenciados (**Administrador** y **Cliente**) para proteger las funciones críticas.
* **📊 Dashboard Estadístico:** Visualización de datos mediante gráficas comparativas (Stock Actual vs. Objetivo) para la toma de decisiones estratégicas.
* **📄 Reportes PDF:** Generación dinámica de reportes de inventario y vales de resguardo listos para imprimir.

## 🛠️ Stack Tecnológico

La aplicación utiliza una arquitectura modular basada en el ecosistema **Python**:

* **Backend:** Python 3.12, Flask (Micro-framework).
* **Base de Datos:** SQLite (Desarrollo) gestionada con **SQLAlchemy** (ORM).
* **Frontend:** HTML5, CSS3 (**Bootstrap 5**, **Animate.css**) y Jinja2.
* **Visualización de Datos:** Chart.js.

### Librerías Clave
* `Flask-Login`: Gestión de sesiones y seguridad.
* `Flask-Migrate`: Control de versiones de base de datos.
* `Flask-Mail`: Sistema de notificaciones por correo.
* `xhtml2pdf`: Generación de reportes PDF.

## 🗄️ Modelo de Datos
El sistema implementa un modelo relacional con 4 tablas principales:
1.  **User:** Credenciales y roles.
2.  **Product:** Inventario, precios y stock.
3.  **Supplier:** Datos fiscales de proveedores.
4.  **Sale:** Historial transaccional.
5.  **Product_Supplier:** Tabla de asociación (Muchos a Muchos).

## 🔧 Manual de Instalación

Sigue estos pasos para desplegar el proyecto en local:

1.  **Clonar el repositorio y acceder a la carpeta:**
    ```bash
    git clone [https://github.com/joce-ortiz/app-suministros-informaticos.git](https://github.com/joce-ortiz/app-suministros-informaticos.git)
    cd app-suministros-informaticos
    ```

2.  **Crear y activar entorno virtual:**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicializar la Base de Datos:**
    ```bash
    flask db upgrade
    ```

5.  **Ejecutar la aplicación:**
    ```bash
    python run.py
    ```

6.  **Acceder:**
    Abre tu navegador en `http://127.0.0.1:5000`.

## 🔮 Futuras Mejoras
* Implementación de API RESTful para apps móviles.
* Integración con pasarelas de pago (Stripe/PayPal).
* Recuperación de contraseñas vía token.

---
**Autor:** Jocelyn Ortiz
**Fecha:** 28-11-2025
