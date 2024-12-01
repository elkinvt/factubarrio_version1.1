from flask import render_template
from flask_controller import FlaskController

class Errores_Controller(FlaskController):
    @staticmethod
    def register_error_handlers(app):
        """Registra manejadores de errores personalizados."""

        @app.errorhandler(401)
        def unauthorized(error):
            """Manejador para errores 401 (No autenticado)."""
            return render_template('form_error_401.html', message="Debes iniciar sesión para acceder a esta página.", titulo_pagina="Error de sesion"),  401

        @app.errorhandler(403)
        def forbidden(error):
            """Manejador para errores 403 (Acceso denegado)."""
            return render_template('form_error_403.html', message="No tienes permisos para acceder a esta página.", titulo_pagina="Acceso denegado"), 403
