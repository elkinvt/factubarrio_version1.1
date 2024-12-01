from flask import flash, redirect, request, render_template , url_for, jsonify
from flask_controller import FlaskController

from src.app import app
from src.controllers.decorators import role_required
from src.models.categorias import Categoria #Importar el modelo de categorias
from src.models.productos import Productos  # Importa el modelo de Productos
from src.models.unidad_medida import UnidadMedida #Importar el modelo unidad medida

class Productos_Controller(FlaskController):

    # Ruta para ver productos
    @app.route('/productos_ver', methods=['GET'])
    @role_required(['administrador','vendedor'])
    def productos_ver():
        try:
            # Usar el método que obtienes con el JOIN de productos, categorías y unidades de medida
            productos = Productos.obtener_productos()

            # Formatear el precio con separadores de miles y dos decimales
            for producto_dict in productos:
                producto = producto_dict['producto']
                if producto['precio_unitario'] is not None:
                    producto['precio_unitario_formateado'] = "{:,.2f}".format(producto['precio_unitario'])
                else:
                    producto['precio_unitario_formateado'] = "N/A"

        except Exception as e:
            flash(f'Error al obtener productos: {str(e)}', 'danger')
            productos = []  # En caso de error, asignamos una lista vacía para evitar fallos en la vista

        return render_template('form_ver_producto.html', titulo_pagina="Ver Productos", productos=productos)

    #-------------------

    # Ruta para crear un producto (GET para mostrar formulario, POST para recibir datos)
    @app.route('/productos_crear', methods=['GET', 'POST'])
    @role_required(['administrador'])
    def productos_crear():
        
        if request.method == 'POST':
            # Recibe los datos enviados desde el formulario
            codigo = request.form['codigoProducto']
            nombre = request.form['nombreProducto'].capitalize()
            descripcion = request.form['descripcionProducto'].capitalize()
            categoria = request.form['categoriaProducto']
            precio_unitario = float(request.form['precioProducto'].replace(',', ''))
            unidad_medida = request.form['unidadMedidaProducto']
            presentacion = request.form['presentacionProducto']
            cantidad_stock = int(request.form['cantidadStockProducto'])
            

            # Validaciones y mensajes de error
            errores = {}

            # Validación de Código
            if not codigo:
                errores['codigoProducto'] = 'El código del producto es obligatorio.'
            elif Productos.existe_codigo(codigo):
                errores['codigoProducto'] = 'El código del producto ya existe.'

            # Validación de Nombre
            if not nombre:
                errores['nombreProducto'] = 'El nombre del producto es obligatorio.'
            elif len(nombre) < 3 or len(nombre) > 50:
                errores['nombreProducto'] = 'El nombre debe tener entre 3 y 50 caracteres.'


            # Validación de Descripción
            if not descripcion:
                errores['descripcionProducto'] = 'La descripción es obligatoria.'
            elif len(descripcion) <3 or len(descripcion) > 250:
                errores['descripcionProducto'] = 'la descripcion debe tener entre 3 y 50 caracteres.'

            # Validación de Precio
            try:
                if precio_unitario <= 0 or precio_unitario > 20000000:
                    errores['precioProducto'] = 'El precio debe ser mayor a 0 y menor a 20,000,000.'
                else:
                    # Redondeamos a dos decimales si el precio es válido
                    precio_unitario = round(precio_unitario, 2)
            except ValueError:
                errores['precioProducto'] = 'Precio no válido.'

            # Validación de Cantidad en Stock
            try:
                if cantidad_stock <= 0:
                    errores['cantidadStockProducto'] = 'La cantidad en stock debe ser mayor a cero.'
            except ValueError:
                errores['cantidadStockProducto'] = 'Cantidad en stock no válida.'
            
            # Validación de Categoría
            if not categoria:
                errores['categoriaProducto'] = 'La categoría es obligatoria.'
            elif not Categoria.existe_categoria(categoria):
                errores['categoriaProducto'] = 'La categoría seleccionada no es válida.'

            # Validación de Unidad de Medida
            if not unidad_medida:
                errores['unidadMedidaProducto'] = 'La unidad de medida es obligatoria.'
            elif not UnidadMedida.existe_unidad(unidad_medida):
                errores['unidadMedidaProducto'] = 'La unidad de medida seleccionada no es válida.'

            # Si hay errores, devolvemos JSON con errores
            if errores:
                return jsonify({'status': 'error', 'errores': errores}), 400

            
            # Crea una nueva instancia de Productos
            nuevo_producto = Productos(
                codigo=codigo,
                nombre=nombre,
                descripcion=descripcion,
                categoria_idcategoria=categoria,
                unidad_medida_idunidad_medida=unidad_medida,
                presentacion=presentacion,
                cantidad_stock=cantidad_stock,
                precio_unitario=precio_unitario  # Guardamos el precio redondeado
            )

            try:
                Productos.agregar_producto(nuevo_producto)
                return jsonify({'success': True, 'message': 'Producto creado con éxito'}), 200
            except Exception as e:
                 return jsonify({'success': False, 'message': f'Error al crear producto: {str(e)}'}), 500

        
        try:
            # Usar los métodos del modelo para obtener las categorías y unidades de medida
            categorias = Categoria.obtener_todas()  # Método en el modelo Categoria
            unidades_padre, subunidades = UnidadMedida.obtener_todas_con_subunidades()  # Método en el modelo UnidadMedida

        except Exception as e:
            flash(f'Error al cargar datos: {str(e)}', 'danger')

        return render_template('form_crear_producto.html', categorias=categorias, unidades_padre=unidades_padre, subunidades=subunidades, titulo_pagina="Crear Producto")

    #------------------
    
    # Ruta para buscar o seleccionar el producto
    @app.route('/productos_editar', methods=['GET'])
    @role_required(['administrador'])
    def productos_editar():
        
        # Obtener el término de búsqueda (si existe)
        termino = request.args.get('termino', '').lower()
        producto_id = request.args.get('producto_id')  # ID del producto seleccionado

        try:
            # Fase 1: Si no hay término ni producto_id, mostramos solo el formulario de búsqueda
            if not termino and not producto_id:
                return render_template('form_editar_producto.html', productos=[], producto=None, 
                                    titulo_pagina="Buscar Producto")

            # Fase 2: Si hay término, buscar los productos correspondientes
            if termino:
                productos = Productos.buscar_por_codigo_o_nombre(termino)

                # Si no se encuentran productos, mostramos un mensaje flash
                if not productos:
                    flash('No se encontraron productos con ese nombre o código', 'warning')

                # Mostrar resultados de búsqueda, pero sin formulario de edición aún
                return render_template('form_editar_producto.html', productos=productos, producto=None, 
                                    titulo_pagina="Seleccionar Producto")

            # Fase 3: Si se seleccionó un producto por ID, cargar los detalles del producto
            if producto_id:
                producto = Productos.obtener_por_id(producto_id)
                categorias = Categoria.obtener_todas()
                unidades_padre, subunidades = UnidadMedida.obtener_todas_con_subunidades()

                # Mostrar el formulario de edición con los detalles del producto seleccionado
                return render_template('form_editar_producto.html', productos=[], producto=producto, 
                                    categorias=categorias, unidades_padre=unidades_padre, subunidades=subunidades, 
                                    titulo_pagina="Editar Producto")

        except Exception as e:
            flash(f'Error al procesar la solicitud: {str(e)}', 'danger')
            return render_template('form_editar_producto.html', productos=[], producto=None, 
                                titulo_pagina="Error")

    #--------------------

    # Ruta para mostrar el formulario con los datos del producto a editar
    @app.route('/productos_editar/<int:id>', methods=['GET'])
    def mostrar_formulario_editar_producto(id):
        try:
            # Usar el método del modelo para obtener el producto por ID
            producto = Productos.obtener_por_id(id)
            categorias = Categoria.obtener_todas()   # Obtener todas las categorías
            unidades_padre, subunidades = UnidadMedida.obtener_todas_con_subunidades()  # Obtener todas las unidades de medida

            if producto:
                # Pasar los datos del producto a la plantilla
                return render_template('form_editar_producto.html', producto=producto, categorias=categorias, unidades_padre=unidades_padre, 
            subunidades=subunidades, titulo_pagina="Editar Producto ")
            else:
                flash('Producto no encontrado.', 'danger')
                return redirect(url_for('productos_editar'))
            
        except Exception as e:
            flash(f'Error al cargar datos: {str(e)}', 'danger')
            return redirect(url_for('productos_editar'))
        
    #--------------------------

    # Ruta para actualizar el producto (POST) usando AJAX
    @app.route('/productos_actualizar/<int:id>', methods=['POST'])
    @role_required(['administrador'])
    def actualizar_producto(id):

        errores = {}  # Diccionario para almacenar errores específicos de cada campo
        try:
            # Validaciones de los datos recibidos
            codigo = request.form['codigo']
            nombre = request.form['nombre'].capitalize()
            descripcion = request.form['descripcion'].capitalize()
            categoria_id = request.form['categoria_id']
            precio_unitario = float(request.form['precio'])
            unidad_medida_id = request.form['unidadMedidaProducto']
            presentacion = request.form['presentacion']
            cantidad_stock = int(request.form['cantidad_stock'])

            # Validación de Código
            if not codigo:
                errores['codigo'] = 'El código es obligatorio.'
            elif Productos.existe_codigo(codigo) and Productos.obtener_por_id(id)['codigo'] != codigo:
                errores['codigo'] = 'El código ya está en uso por otro producto.'

            # Validación de Nombre
            if not nombre:
                errores['nombre'] = 'El nombre es obligatorio.'
            elif len(nombre) < 3 or len(nombre) > 50:
                errores['nombre'] = 'El nombre debe tener entre 3 y 50 caracteres.'

            # Validación de Descripción
            if not descripcion:
                errores['descripcionProducto'] = 'La descripción es obligatoria.'
            elif len(descripcion) <3 or len(descripcion) > 250:
                errores['descripcion'] = 'la descripcion debe tener entre 3 y 50 caracteres.'

            # Validación de Categoría y Unidad de Medida
            if not Categoria.existe_categoria(categoria_id):
                errores['categoria_id'] = 'La categoría seleccionada no existe.'
            if not UnidadMedida.existe_unidad(unidad_medida_id):
                errores['unidadMedidaProducto'] = 'La unidad de medida seleccionada no existe.'

            # Validación de Presentación
            if not presentacion:
                errores['presentacion'] = 'La presentación es obligatoria.'

            # Validación de Cantidad en Stock
            try:
                if cantidad_stock < 1:
                    errores['cantidad_stock'] = 'La cantidad en stock debe ser mayor a cero.'
            except ValueError:
                errores['cantidad_stock'] = 'Cantidad en stock no válida.'

            # Validación de Precio Unitario
            try:
                if precio_unitario <= 0 or precio_unitario > 20000000:
                    errores['precio'] = 'El precio unitario debe ser mayor a cero.'
                else:
                    # Redondeamos a dos decimales si el precio es válido
                    precio_unitario = round(precio_unitario, 2)
            except ValueError:
                errores['precio'] = 'Precio unitario no válido.'


            # Verificación de errores antes de proceder con la actualización
            if errores:
                return jsonify({'success': False, 'errors': errores}), 400  # Enviamos los errores específicos como respuesta JSON

            # Diccionario de datos actualizados
            datos_actualizados = {
                'codigo': codigo,
                'nombre': nombre,
                'descripcion': descripcion,
                'categoria_idcategoria': categoria_id,
                'unidad_medida_idunidad_medida': unidad_medida_id,
                'presentacion': presentacion,
                'cantidad_stock': cantidad_stock,
                'precio_unitario': precio_unitario
            }

            # Usamos el método del modelo para actualizar el producto
            producto = Productos.actualizar_producto(id, datos_actualizados)
            if producto:
                return jsonify({'success': True, 'message': 'Producto actualizado correctamente.'}), 200
            else:
                return jsonify({'success': False, 'errors': {'general': 'Producto no encontrado.'}}), 404

        except Exception as e:
            return jsonify({'success': False, 'errors': {'general': f'Error al actualizar producto: {str(e)}'}}), 500

    #---------------

    # Ruta para actualizar el estado de un producto
    @app.route('/productos_toggle_estado', methods=['POST'])
    @role_required(['administrador'])
    def toggle_estado_producto():
        id_producto = request.form.get('idproducto')  # Recibir el ID del producto desde el formulario

        # Validaciones y mensajes de error
        errores = {}

        # Validación del ID del producto
        if not id_producto:
            errores['idproducto'] = 'El ID del producto es obligatorio.'
        elif not id_producto.isdigit():
            errores['idproducto'] = 'El ID del producto debe ser un número válido.'

        # Si hay errores, devolvemos JSON con los errores
        if errores:
            return jsonify({'status': 'error', 'errores': errores}), 400

        # Intento de actualización del estado
        try:
            # Llamar al método del modelo para cambiar el estado
            nuevo_estado = Productos.toggle_estado(int(id_producto))
            
            if nuevo_estado is None:
                return jsonify({'success': False, 'message': 'Producto no encontrado.'}), 404
            
            estado_texto = 'activado' if nuevo_estado else 'desactivado'
            return jsonify({'success': True, 'message': f'Producto {estado_texto} con éxito.'}), 200
        
        except Exception as e:
            return jsonify({'success': False, 'message': f'Ocurrió un error al intentar cambiar el estado del producto: {str(e)}'}), 500

    #------------------
    
    # Ruta para eliminar un producto (eliminación lógica)
    @app.route('/productos_eliminar', methods=['POST'])
    @role_required(['administrador'])
    def eliminar_producto():
        id_producto = request.form['idProducto']  # Obtener el ID del producto desde el formulario

         # Validaciones y mensajes de error
        errores = {}

        # Validación del ID del producto
        if not id_producto:
            errores['idproducto'] = 'El ID del producto es obligatorio.'
        elif not id_producto.isdigit():
            errores['idproducto'] = 'El ID del producto debe ser un número válido.'

        # Si hay errores, devolvemos JSON con los errores
        if errores:
            return jsonify({'status': 'error', 'errores': errores}), 400
        
        # Intento de eliminacion logica
        try:
            # Usar el método en el modelo para obtener el producto por ID
            eliminado = Productos.eliminar_producto(id_producto)
            
            if eliminado:
                # Producto eliminado con éxito
                return jsonify({'success': True, 'message': 'Producto eliminado con éxito.'}), 200
            else:
                # Producto no encontrado
                return jsonify({'success': False, 'message': 'Producto no encontrado.'}), 404

        except Exception as e:
            # Error inesperado
            return jsonify({'success': False, 'message': f'Error al eliminar el producto: {str(e)}'}), 500
    
    #------------------
    
    # Ruta para agregar los productos a la factura
    @app.route('/buscar_productos')
    def buscar_productos():
        query = request.args.get('q', '').lower()
        
        try:
            
            productos_data = Productos.buscar_productos_por_nombre(query)
            return jsonify(productos_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    #-------------------

    # Ruta para verificar producto y stock
    @app.route('/verificar_producto')
    def verificar_producto():
        codigo = request.args.get('codigo')
        cantidad = int(request.args.get('cantidad'))

        try:
            # Llamar al método del modelo para verificar el producto y su stock
            resultado = Productos.verificar_stock_producto(codigo, cantidad)

            # Verificar si hay algún error en el resultado
            if 'error' in resultado:
                return jsonify(resultado), 200
            else:
                return jsonify(resultado)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
 
    #--------------