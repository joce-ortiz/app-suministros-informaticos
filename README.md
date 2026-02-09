# 💻 Aplicación de Gestión para Empresa de Suministros Informáticos

**Proyecto Final - Curso de Programación Python**

## 📖 Descripción General
[cite_start]Este proyecto consiste en el desarrollo de una aplicación web "Full Stack" para la gestión integral de una empresa de suministros informáticos[cite: 10]. [cite_start]La solución nace de la necesidad de digitalizar y optimizar el control de inventario, la gestión de proveedores y el registro de ventas[cite: 11].

[cite_start]La plataforma permite a los administradores mantener un control estricto sobre el stock, recibir alertas automáticas y analizar el rendimiento del negocio, mientras ofrece una interfaz para que los clientes consulten el catálogo y realicen pedidos[cite: 12, 13].

## 🚀 Objetivos y Funcionalidades Clave

* [cite_start]**📦 Digitalización del Inventario:** Operaciones CRUD (Crear, Leer, Actualizar, Borrar) completas sobre productos y proveedores[cite: 18].
* [cite_start]**⚠️ Automatización de Alertas:** Sistema proactivo que notifica vía correo electrónico (SMTP) cuando el stock de un producto desciende del **10%** de su objetivo[cite: 19].
* [cite_start]**🔐 Seguridad y Roles:** Sistema de autenticación con roles diferenciados (**Administrador** y **Cliente**) para proteger las funciones críticas[cite: 20].
* [cite_start]**📊 Dashboard Estadístico:** Visualización de datos mediante gráficas comparativas (Stock Actual vs. Objetivo) para la toma de decisiones estratégicas[cite: 21].
* [cite_start]**📄 Reportes PDF:** Generación dinámica de reportes de inventario y vales de resguardo listos para imprimir[cite: 25, 40].

## 🛠️ Stack Tecnológico

[cite_start]La aplicación utiliza una arquitectura modular basada en el ecosistema **Python**[cite: 30]:

* [cite_start]**Backend:** Python 3.12, Flask (Micro-framework)[cite: 31, 32].
* [cite_start]**Base de Datos:** SQLite (Desarrollo) gestionada con **SQLAlchemy** (ORM)[cite: 33].
* [cite_start]**Frontend:** HTML5, CSS3 (**Bootstrap 5**, **Animate.css**) y Jinja2[cite: 34].
* [cite_start]**Visualización de Datos:** Chart.js[cite: 39].

### Librerías Clave
* [cite_start]`Flask-Login`: Gestión de sesiones y seguridad[cite: 36].
* [cite_start]`Flask-Migrate`: Control de versiones de base de datos[cite: 37].
* [cite_start]`Flask-Mail`: Sistema de notificaciones por correo[cite: 38].
* [cite_start]`xhtml2pdf`: Generación de reportes PDF[cite: 40].

## 🗄️ Modelo de Datos
[cite_start]El sistema implementa un modelo relacional con 4 tablas principales[cite: 52]:
1.  [cite_start]**User:** Credenciales y roles[cite: 53].
2.  [cite_start]**Product:** Inventario, precios y stock[cite: 54].
3.  [cite_start]**Supplier:** Datos fiscales de proveedores[cite: 55].
4.  [cite_start]**Sale:** Historial transaccional[cite: 57].
5.  [cite_start]**Product_Supplier:** Tabla de asociación (Muchos a Muchos)[cite: 58].

## 🔧 Manual de Instalación

[cite_start]Sigue estos pasos para desplegar el proyecto en local[cite: 80]:

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
    [cite_start][cite: 85, 88, 91]

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    [cite_start][cite: 94]

4.  **Inicializar la Base de Datos:**
    ```bash
    flask db upgrade
    ```
    [cite_start][cite: 98]

5.  **Ejecutar la aplicación:**
    ```bash
    python run.py
    ```
    [cite_start][cite: 102]

6.  **Acceder:**
    [cite_start]Abre tu navegador en `http://127.0.0.1:5000`[cite: 104].

## 🔮 Futuras Mejoras
* Implementación de API RESTful para apps móviles[cite: 112].
* [cite_start]Integración con pasarelas de pago (Stripe/PayPal)[cite: 113].
* [cite_start]Recuperación de contraseñas vía token[cite: 113].

---
[cite_start]**Autor:** Jocelyn Ortiz [cite: 6]
[cite_start]**Fecha:** 28-11-2025 [cite: 7]
