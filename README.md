# FactuBarrio 1.1

**FactuBarrio** es un sistema web de facturación desarrollado como proyecto académico en el marco del programa de Análisis y Desarrollo de Software del SENA.  
La aplicación permite gestionar productos, clientes, facturas y usuarios, utilizando una arquitectura tipo **MVC** y una base de datos **PostgreSQL**.

> ⚠️ Proyecto en desarrollo. No implementa medidas de seguridad avanzadas. Ideal para fines educativos, pruebas o como base para futuros desarrollos más robustos.

---

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **Flask**
- **Flask-Login**
- **PostgreSQL**
- **SQLAlchemy**
- **HTML/CSS/Bootstrap**
- **Jinja2 (para plantillas)**

---

## ✨ Funcionalidades principales

- Gestión de usuarios (con roles)
- CRUD de productos y clientes
- Generación y consulta de facturas
- Navegación con controladores organizados
- Arquitectura basada en MVC

---

## 🚀 Cómo ejecutar el proyecto

1. Clona este repositorio:
```bash
git clone https://github.com/elkinvt/FactuBarrio.git

2. Instala los requerimientos:
pip install -r requirements.txt

3. Configura la base de datos PostgreSQL según los parámetros del archivo .Env(entorno_virtual) o configuración interna.
4.Ejecuta la aplicación:
python app.py

📌 Notas
•	Proyecto desarrollado como práctica académica.
•	No se han implementado filtros de seguridad como validación CSRF, manejo de errores avanzados o cifrado de contraseñas.
•	Está diseñado para seguir evolucionando y escalar en futuras versiones.
👤 Autor
Elkin Vasquez
Estudiante de Análisis y Desarrollo de Software
GitHub: elkinvt
