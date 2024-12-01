from flask import flash, render_template, request, jsonify
from flask_controller import FlaskController

from src.app import app
from src.controllers.decorators import role_required
from src.models.usuarios import Usuarios  

class Usuarios_Controller(FlaskController):

    # Ruta para ver todos los usuarios
    @app.route('/usuarios_ver', methods=['GET'])
    @role_required(['administrador'])
    def usuarios_ver():
        usuarios = Usuarios.obtener_usuarios()
        return render_template('form_ver_usuario.html', titulo_pagina="Ver usurios", usuarios=usuarios)

    #--------------

    # Ruta para crear el usuario
    @app.route('/usuarios_crear', methods=['GET', 'POST'])
    @role_required(['administrador'])
    def usuarios_crear():
        if request.method == 'GET':
            return render_template('form_crear_usuario.html', titulo_pagina="Crear usuario")

        if request.method == 'POST':
            # Extrae los datos del formulario
            nombre = request.form.get('nombre').title()
            email = request.form.get('email')
            contraseña = request.form.get('contraseña')
            rol = request.form.get('rol')

            # Diccionario para almacenar errores de validación
            errores = {}

            # Validaciones de los campos
            if not nombre:
                errores['nombre'] = 'El nombre es obligatorio.'
            elif len(nombre) < 3 or len(nombre) > 50:
                errores['nombre'] = 'Debe tener entre 3 y 50 caracteres.'

            if not email:
                errores['email'] = 'El email es obligatorio.'
            elif "@" not in email or "." not in email.split("@")[-1]:
                errores['email'] = 'Debe ser un email válido.'
            else:
                # Verificación de duplicados de email
                if Usuarios.validar_datos(email=email):  # Método que verifica si el email ya existe
                    errores['email'] = 'El email ya está registrado.'

            if not contraseña:
                errores['contraseña'] = 'La contraseña es obligatoria.'
            elif len(contraseña) < 8:
                errores['contraseña'] = 'Debe tener al menos 8 caracteres.'

            if not rol:
                errores['rol'] = 'El rol es obligatorio.'
            elif rol not in ['administrador', 'vendedor']:
                errores['rol'] = 'El rol debe ser "administrador" o "vendedor".'

            # Si hay errores, devolvemos JSON con errores
            if errores:
                return jsonify({'status': 'error', 'errores': errores}), 400

            # Crear el objeto usuario con los datos del formulario
            nuevo_usuario = Usuarios(
                nombre_usuario=nombre,
                email=email,
                contraseña=contraseña,
                rol=rol
            )

            try:
                # Llama al método agregar_usuario para guardar el usuario en la base de datos
                Usuarios.agregar_usuario(nuevo_usuario)
                return jsonify({'success': True, 'message': 'Usuario creado exitosamente'}), 200
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error al crear usuario: {str(e)}'}), 500

    #-------------

    # Ruta para mostrar el formulario de edición de usuario (GET)
    @app.route('/usuarios_editar', methods=['GET'])
    @role_required(['administrador'])
    def usuarios_editar():
        nombre_usuario = request.args.get('nombre')  # Obtener el nombre del usuario desde los parámetros de la URL

        if not nombre_usuario:
            flash('Por favor, proporcione el nombre del usuario.', 'warning')
            return render_template('form_editar_usuario.html', usuario=None, titulo_pagina="Editar Usuario")

        try:
            # Llamar al método del modelo para buscar el usuario por nombre sin manejar la sesión
            usuario = Usuarios.buscar_usuario_por_nombre(nombre_usuario)
            
            if usuario:
                if usuario['is_deleted']:
                    flash('Este usuario ha sido eliminado y no puede ser editado.', 'danger')
                    return render_template('form_editar_usuario.html', usuario=None, titulo_pagina="Usuario Eliminado")
                
                return render_template('form_editar_usuario.html', usuario=usuario, titulo_pagina="Editar Usuario")
            else:
                flash('Usuario no encontrado. Verifique el nombre proporcionado.', 'danger')
                return render_template('form_editar_usuario.html', usuario=None, titulo_pagina="Editar Usuario")
            
        except Exception as e:
            flash(f'Error al buscar el usuario: {str(e)}', 'danger')
            return render_template('form_editar_usuario.html', usuario=None, titulo_pagina="Error al Editar Usuario")
    #--------

    # Ruta para actualizar un usuario (POST)
    @app.route('/usuarios_actualizar', methods=['POST'])
    @role_required(['administrador'])
    def actualizar_usuarios():

        usuario_id = request.form.get['usuarioId']
        nombre_usuario = request.form.get['nombreUsuario'].title()
        email = request.form.get['emailUsuario']
        rol = request.form.get['rolUsuario']
        is_active = request.form.get['estadousuario'].lower() == 'activo'
        nueva_contraseña = request.form.get('nuevaContraseña')
        confirmar_contraseña = request.form.get('confirmarContraseña')

         # Diccionario de errores específicos por campo
        errores = {}

        # Validaciones
        if not nombre_usuario:
            errores['nombreUsuario'] = 'El nombre es obligatorio.'
        elif len(nombre_usuario) < 3 or len(nombre_usuario) > 50:
            errores['nombreUsuario'] = 'Debe tener entre 3 y 50 caracteres.'
        
        if not email:
            errores['emailUsuario'] = 'El email es obligatorio.'
        elif "@" not in email or "." not in email.split("@")[-1]:
            errores['emailUsuario'] = 'Debe ser un email válido.'

        if nueva_contraseña:
            if nueva_contraseña != confirmar_contraseña:
                errores['confirmarContraseña'] = 'Las contraseñas no coinciden.'
            elif len(nueva_contraseña) < 8:
                errores['nuevaContraseña'] = 'La contraseña debe tener al menos 8 caracteres.'

        # Validación de duplicados, excluyendo el usuario actual
        duplicados = Usuarios.validar_datos(email=email, usuario_id=usuario_id)
        if duplicados:
            errores.update(duplicados)

        # Si hay errores, devolver un JSON con los errores
        if errores:
            return jsonify({'status': 'error', 'errores': errores}), 400

        # Diccionario de datos actualizados
        datos_actualizados = {
            'nombres_usuario': nombre_usuario,
            'email': email,
            'rol': rol,
            'is_active': is_active
        }

        # Agregar la contraseña solo si se proporciona
        if nueva_contraseña:
            datos_actualizados['contraseña'] = nueva_contraseña

        try:
            Usuarios.actualizar_usuario(usuario_id, datos_actualizados)
            return jsonify({'status': 'success', 'message': 'Usuario actualizado con éxito'}), 200
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Usuario no encontrado.'}), 404
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Error al actualizar usuario: {str(e)}'}), 500
    
    #--------------------

    # Ruta para verificar el email del usuario
    @app.route('/usuarios/verificar_email', methods=['GET'])
    def verificar_email():
        email = request.args.get('email')
        usuario_id = request.args.get('usuario_id')  # Opcional, si quieres excluir un usuario específico

        # Usa el método `validar_datos` para comprobar si el email ya está en uso
        duplicados = Usuarios.validar_datos(email=email, usuario_id=usuario_id)
        
        # Comprueba si hay errores relacionados con el email en `duplicados`
        if 'emailUsuario' in duplicados:
            return jsonify({'exists': True})
        else:
            return jsonify({'exists': False})

    #---------

    # Ruta para actualizar el estado de un usuario
    @app.route('/usuario_toggle_estado', methods=['POST'])
    @role_required(['administrador'])
    def toggle_estado_usuario():
        id_usuario = request.form.get('id_usuario')  # Usar el ID del usuario

        # Validar que se reciba un ID válido
        if not id_usuario:
            return jsonify({'status': 'error', 'message': 'ID de usuario es obligatorio.'}), 400

        
        # Intento de actualización del estado
        try:
            nuevo_estado = Usuarios.actualizar_estado(id_usuario)
            
            if nuevo_estado is None:
                return jsonify({'success': False, 'message': 'Usuario no encontrado.'}), 404
            
            estado_texto = 'activado' if nuevo_estado else 'desactivado'
            return jsonify({'success': True, 'message': f'Usuario {estado_texto} con éxito.'}), 200
        
        except Exception as e:
            return jsonify({'success': False, 'message': f'Ocurrió un error al intentar cambiar el estado del usuario: {str(e)}'}), 500

    #----------

    # Ruta para eliminar usuario (lógica)
    @app.route('/usuario_eliminar', methods=['POST'])
    @role_required(['administrador'])
    def eliminar_usuario():
        id_usuario = request.form.get('id_usuario')

        # Validar que se reciba un ID válido
        if not id_usuario:
            return jsonify({'status': 'error', 'message': 'ID de usuario es obligatorio.'}), 400

        # Intento de eliminación lógica del usuario
        try:
            eliminado = Usuarios.eliminar_usuario_logicamente(id_usuario)
            
            if not eliminado:
                return jsonify({'success': False, 'message': 'Usuario no encontrado o ya eliminado.'}), 404
            
            return jsonify({'success': True, 'message': 'Usuario eliminado correctamente.'}), 200
        
        except Exception as e:
            return jsonify({'success': False, 'message': f'Ocurrió un error al intentar eliminar el usuario: {str(e)}'}), 500

    #-----------