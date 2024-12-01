from flask import flash, jsonify, request, render_template
from flask_controller import FlaskController

from src.app import app
from src.models.clientes import Clientes
from src.controllers.decorators import role_required

class Clientes_Controller(FlaskController):
    
    # Ruta para ver todos los clientes
    @app.route('/clientes_ver', methods=['GET'])
    @role_required(['administrador','vendedor']) 
    def clientes_ver():
        clientes = Clientes.obtener_clientes()
        return render_template('form_ver_cliente.html', titulo_pagina="Ver Clientes", clientes=clientes)

    #----------------------------------

    # Ruta para crear el cliente
    @app.route('/clientes_crear', methods=['GET', 'POST'])
    @role_required(['administrador'])
    def clientes_crear():
        if request.method == 'GET':
            return render_template('form_crear_cliente.html', titulo_pagina="Crear Cliente")
        if request.method == 'POST':
            tipo_documento = request.form['tipoDocumento']
            numero_documento = request.form['numeroDocumento']
            nombre_completo = request.form['nombreCliente'].title()
            telefono = request.form['telefonoCliente']
            direccion = request.form['direccionCliente']
            email = request.form['emailCliente']

            # Validaciones y mensajes de error
            errores = {}

            # Validación del tipo de documento
            if not tipo_documento:
                errores['tipoDocumento'] = 'El tipo de documento es obligatorio.'
            elif not tipo_documento.isalpha():
                errores['tipoDocumento'] = 'El tipo de documento debe contener solo letras.'

            # Validación del número de documento
            if not numero_documento:
                errores['numeroDocumento'] = 'El número de documento es obligatorio.'
            elif not numero_documento.isdigit():
                errores['numeroDocumento'] = 'Debe contener solo números.'
            elif len(numero_documento) < 6 or len(numero_documento) > 15:
                errores['numeroDocumento'] = 'Debe tener entre 6 y 15 dígitos.'

            # Validación del nombre completo
            if not nombre_completo:
                errores['nombreCliente'] = 'El nombre es obligatorio.'
            elif len(nombre_completo) < 3 or len(nombre_completo) > 50:
                errores['nombreCliente'] = 'Debe tener entre 3 y 50 caracteres.'

            # Validación del teléfono
            if not telefono:
                errores['telefonoCliente'] = 'El teléfono es obligatorio.'
            elif not telefono.isdigit():
                errores['telefonoCliente'] = 'Debe contener solo números.'
            elif len(telefono) < 10:
                errores['telefonoCliente'] = 'Debe tener al menos 10 dígitos.'

            # Validación de la dirección
            if not direccion:
                errores['direccionCliente'] = 'La dirección es obligatoria.'
            elif len(direccion) < 10:
                errores['direccionCliente'] = 'Debe tener al menos 10 caracteres.'

            # Validación del email
            if not email:
                errores['emailCliente'] = 'El email es obligatorio.'
            elif "@" not in email or "." not in email.split("@")[-1]:
                errores['emailCliente'] = 'Debe ser un email válido.'

            # Validación de duplicados
            duplicados = Clientes.validar_datos(numero_documento=numero_documento, email=email)
            if duplicados:
                errores.update(duplicados)

            # Si hay errores, devolvemos JSON con errores
            if errores:
                return jsonify({'status': 'error', 'errores': errores}), 400

            # Si todas las validaciones pasan, intentamos crear el cliente
            nuevo_cliente = Clientes(
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
                nombres_cliente=nombre_completo,
                telefono=telefono,
                direccion=direccion,
                email=email,
                is_active=True,
                is_deleted=False
            )

            try:
                Clientes.agregar_cliente(nuevo_cliente)
                return jsonify({'success': True, 'message': 'Cliente creado con éxito'}), 200
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error al crear cliente: {str(e)}'}), 500


    #------------------------

    # Ruta para mostrar el formulario de edición (GET)  
    @app.route('/clientes_editar', methods=['GET'])
    @role_required(['administrador'])
    def clientes_editar():
        numero_documento = request.args.get('numeroDocumento')

        if  not numero_documento:
            flash('Por favor, ingrese número de Documento.', 'warning')
            return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Editar Cliente")

        try:
            # Llamar al método del modelo para buscar el cliente sin manejar la sesión
            cliente = Clientes.buscar_cliente_por_documento(numero_documento)
            
            if cliente:
                if cliente['is_deleted']:
                    flash('Este cliente ha sido eliminado y no puede ser editado.', 'danger')
                    return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Cliente Eliminado")
                return render_template('form_editar_cliente.html', cliente=cliente, titulo_pagina="Editar Cliente")
            else:
                flash('Cliente no encontrado. Verifique los datos ingresados.', 'danger')
                return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Editar Cliente")
            
        except Exception as e:
            flash(f'Error al buscar el cliente: {str(e)}', 'danger')
            return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Error al Editar cliente")

    #---------------------------------

    # Ruta para actualizar un cliente (POST)
    @app.route('/clientes_actualizar', methods=['POST'])
    @role_required(['administrador'])
    def actualizar_cliente():
        cliente_id = request.form['clienteId']
        tipo_documento = request.form['tipoDocumento']
        numero_documento = request.form['numeroDocumento']
        nombre_completo = request.form['nombreCliente'].title()
        telefono = request.form['telefonoCliente']
        direccion = request.form['direccionCliente']
        email = request.form['emailCliente']
        is_active = request.form['estadoCliente'].lower() == 'activo'

        # Diccionario de errores específicos por campo
        errores = {}

        # Validaciones
        if not nombre_completo:
            errores['nombreCliente'] = 'El nombre es obligatorio.'
        elif len(nombre_completo) < 3 or len(nombre_completo) > 50:
            errores['nombreCliente'] = 'Debe tener entre 3 y 50 caracteres.'

        if not telefono:
            errores['telefonoCliente'] = 'El teléfono es obligatorio.'
        elif not telefono.isdigit():
            errores['telefonoCliente'] = 'Debe contener solo números.'
        elif len(telefono) < 10:
            errores['telefonoCliente'] = 'Debe tener al menos 10 dígitos.'

        if not direccion:
            errores['direccionCliente'] = 'La dirección es obligatoria.'
        elif len(direccion) < 10:
            errores['direccionCliente'] = 'Debe tener al menos 10 caracteres.'

        if not email:
            errores['emailCliente'] = 'El email es obligatorio.'
        elif "@" not in email or "." not in email.split("@")[-1]:
            errores['emailCliente'] = 'Debe ser un email válido.'

        # Validación de duplicados, excluyendo el cliente actual
        duplicados = Clientes.validar_datos(numero_documento=numero_documento, email=email, cliente_id=cliente_id)
        if duplicados:
            errores.update(duplicados)

        # Si hay errores, devolver un JSON con los errores
        if errores:
            return jsonify({'status': 'error', 'errores': errores}), 400

        # Diccionario de datos actualizados
        datos_actualizados = {
            'tipo_documento': tipo_documento,
            'numero_documento': numero_documento,
            'nombres_cliente': nombre_completo,
            'telefono': telefono,
            'direccion': direccion,
            'email': email,
            'estadoCliente': is_active
        }

        try:
            Clientes.actualizar_cliente(cliente_id, datos_actualizados)
            return jsonify({'success': True, 'message': 'Cliente actualizado con éxito'}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al actualizar cliente: {str(e)}'}), 500
  
    #--------------------
    
    # Ruta para actualizar el estado de un cliente
    @app.route('/clientes_toggle_estado', methods=['POST'])
    @role_required(['administrador'])
    def toggle_estado_cliente():
        cliente_id = request.form.get('idclientes')
        
        # Validaciones y mensajes de error
        errores = {}

        # Validación del ID del cliente
        if not cliente_id:
            errores['idclientes'] = 'El ID del cliente es obligatorio.'
        elif not cliente_id.isdigit():
            errores['idclientes'] = 'El ID del cliente debe ser un número válido.'
        
        # Si hay errores, devolvemos JSON con errores
        if errores:
            return jsonify({'status': 'error', 'errores': errores}), 400

        # Intento de actualización del estado
        try:
            cliente_id = int(cliente_id)
            nuevo_estado = Clientes.actualizar_estado(cliente_id)
            
            if nuevo_estado is None:
                return jsonify({'success': False, 'message': 'Cliente no encontrado.'}), 404
            
            estado_texto = 'activado' if nuevo_estado else 'desactivado'
            return jsonify({'success': True, 'message': f'Cliente {estado_texto} con éxito.'}), 200
        
        except Exception as e:
            return jsonify({'success': False, 'message': f'Ocurrió un error al intentar cambiar el estado del cliente: {str(e)}'}), 500

    #----------

    # Ruta para eliminar cliente (lógica)
    @app.route('/clientes_eliminar', methods=['POST'])
    @role_required(['administrador'])
    def eliminar_cliente():
        cliente_id = request.form.get('idclientes')

        # Validaciones y mensajes de error
        errores = {}

        # Validación del ID del cliente
        if not cliente_id:
            errores['idclientes'] = 'El ID del cliente es obligatorio.'
        elif not cliente_id.isdigit():
            errores['idclientes'] = 'El ID del cliente debe ser un número válido.'
        
        # Si hay errores, devolvemos JSON con errores
        if errores:
            return jsonify({'status': 'error', 'errores': errores}), 400

        # Intento de eliminación del cliente
        try:
            cliente_id = int(cliente_id)
            if Clientes.eliminar_cliente_logicamente(cliente_id):
                return jsonify({'success': True, 'message': 'Cliente eliminado correctamente.'}), 200
            else:
                return jsonify({'success': False, 'message': 'Cliente no encontrado o ya eliminado.'}), 404
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al eliminar el cliente: {str(e)}'}), 500

    #-----------

    # Ruta para buscar cliente por numero de documento
    @app.route('/buscar_clientes_por_numero_documento')
    def buscar_clientes_por_numero_documento():
        query = request.args.get('q', '').strip()
        
        # Validar que el query no esté vacío
        if not query:
            return jsonify({'error': 'El número de documento es obligatorio.'}), 400
        
        # Validar el formato del query (solo números y longitud específica, por ejemplo)
        if not query.isdigit() or len(query) < 5 or len(query) > 15:
            return jsonify({'error': 'El número de documento debe contener entre 5 y 15 dígitos.'}), 400
        
        try:
            # Buscar clientes en la base de datos
            clientes_activos = Clientes.buscar_clientes(query)
            if clientes_activos:
                return jsonify(clientes_activos)
            
            # Buscar inactivos o eliminados
            cliente_inactivo = Clientes.buscar_clientes(query, incluir_inactivos=True, incluir_eliminados=True)
            if cliente_inactivo:

                cliente = cliente_inactivo[0]  # Asegurar que hay un cliente

                if not cliente['is_active']:
                    return jsonify({'message': 'El cliente está inactivo.'}),403
                
                if cliente['is_deleted']:
                    return jsonify({'message': 'El cliente ha sido eliminado'}),403
                
            return jsonify({'message': 'No se encontraron  cliente con ese número de documento.'}),404
        
        except Exception as e:
            print(f"Error al buscar clientes: {str(e)}")
            # Manejar errores internos
            return jsonify({'error': f'Ocurrió un error: {str(e)}'}), 500
        
    #------------------

    # Ruta para validar los datos de un cliente
    @app.route('/validar_cliente', methods=['POST'])
    def validar_cliente():
        data = request.get_json()
        errores = Clientes.validar_datos(
            numero_documento=data.get('numeroDocumento'),
            email=data.get('emailCliente')
        )
        if errores:
            return jsonify({'status': 'error', 'errores': errores}), 400
        return jsonify({'status': 'success'})
    
    #---------------------


    
