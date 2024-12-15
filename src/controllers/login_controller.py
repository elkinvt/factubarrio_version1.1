from flask import  flash, redirect, render_template, request, url_for, session
from flask_login import login_user
from flask_controller import FlaskController

from src.app import app
from src.models.usuarios import Usuarios
class LoginController(FlaskController):
    @app.route('/', methods=['GET'])
    def home():
        return redirect(url_for('login'))

    @app.route('/login', methods=['POST','GET'])
    def login():    
        if request.method == 'POST':
            nombre_usuario = request.form.get('nombre_usuario')                
            contraseña = request.form.get('contraseña')
            
            # Validar usuario  
            usuario_valido = Usuarios.validar_usuario_login(nombre_usuario, contraseña)
            if usuario_valido:
                # Verificar si el usuario está activo
                #if usuario_valido.is_active != 'False':  # Cambia 'activo' según el valor real en tu base de datos
                    #flash('Tu cuenta está desactivada. Contacta al administrador.', 'danger')
                    #return redirect(url_for('login'))
                
                # Iniciar sesión si el usuario está activo
                login_user(usuario_valido)
                # Guardar el ID del usuario en la sesión
                session['usuario_id'] = usuario_valido.id_usuario  # Asegúrate de que `id_usuario` es el campo correcto
                session['usuario_rol'] = usuario_valido.rol 
                return redirect(url_for('Index'))
            else:
                flash('Nombre de usuario o contraseña incorrectos',  'danger')
                return redirect(url_for('login'))
            
        return render_template('login.html', titulo_pagina = 'Login')