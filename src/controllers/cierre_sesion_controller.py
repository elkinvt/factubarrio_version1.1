from flask import render_template
from flask_controller import FlaskController

from src.app import app 

class Cerra_sesion_Controller(FlaskController):
    @app.route('/cerrar_sesion')
    def cerrar_sesion():
        return render_template('login.html',titulo_pagina = 'Login')