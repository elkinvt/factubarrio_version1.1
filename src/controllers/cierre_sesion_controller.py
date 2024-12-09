from flask import redirect,url_for
from flask_controller import FlaskController

from src.app import app 

class Cerra_sesion_Controller(FlaskController):
    @app.route('/cerrar_sesion')
    def cerrar_sesion():
        return redirect(url_for('login'))