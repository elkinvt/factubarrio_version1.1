from datetime import datetime
import json

from flask import jsonify, render_template, request,   session
from flask_controller import FlaskController


from src.app import app
from src.models.facturas import Factura  # Importar la clase Factura
from src.models.detalle_producto import DetalleProducto  # Importar DetalleProducto
from src.models.productos import Productos  # Importar la clase Productos
from src.models.vendedores import Vendedores  # Importar la clase Vendedores
from src.controllers.decorators import role_required
class Facturas_Controller(FlaskController):

    #Ruta para cargar la vista de facturas
    @app.route('/ver_factura')
    @role_required(['administrador','vendedor']) 
    def ver_factura():
        return render_template('form_ver_factura.html', titulo_pagina = "Ver factura")
    
    #---------

    #Ruta para generar la factura
    @app.route('/generar_factura', methods=['GET', 'POST'])
    @role_required(['vendedor'])
    def generar_factura():
        if request.method == 'POST':
            try:

                # Obtén el usuario logueado (puede ser de `session` o algún middleware)
                usuario_id = session.get('usuario_id')
                print(f"Usuario ID en sesión: {usuario_id}")

                # Obtener el vendedor asociado al usuario
                vendedor = Vendedores.obtener_vendedor_por_usuario(usuario_id)
                if not vendedor:
                    error_message = "No se encontró un vendedor asociado al usuario actual."
                    return render_template('form_error.html', error=error_message), 400
                
                vendedores_idvendedores = vendedor.idvendedores  # Usaremos este vendedor para la factura

                # Recibe los datos del formulario
                clientes_idclientes = request.form.get('clienteId')
                productos = json.loads(request.form.get('productosFactura'))

                # Validación del cliente y vendedor
                if not clientes_idclientes:
                    return jsonify({"error": "Debe seleccionar un cliente válido."}), 400
                if not vendedores_idvendedores:
                    return jsonify({"error": "Debe seleccionar un vendedor válido."}), 400

                # Validación de productos
                if not productos or not isinstance(productos, list):
                    return jsonify({"error": "Debe agregar al menos un producto a la factura."}), 400
                for item in productos: 
                    if 'precio' not in item or 'cantidad' not in item:
                        return jsonify({"error": "Cada producto debe tener un precio y una cantidad."}), 400
                    if float(item['precio']) <= 0 or float(item['precio']) > 20000000:
                        return jsonify({"error": f"El precio de {item['producto']} debe ser mayor a cero y menor a 20,000,000."}), 400
                    if int(item['cantidad']) <= 0:
                        return jsonify({"error": "La cantidad de cada producto debe ser mayor a cero."}), 400

                # Calcular el total de la factura
                total_valor = sum([float(item['precio']) * int(item['cantidad']) for item in productos])
                impuesto = total_valor * 0.19  # Impuesto del 19%
                descuento = float(request.form.get('descuentoFactura', 0))
                if descuento < 0 or descuento > total_valor:
                    return jsonify({"error": "El descuento no puede ser negativo ni mayor al subtotal."}), 400
                total_final = total_valor + impuesto - descuento

                # Recibir los valores de pago y calcular el cambio
                monto_pagado = float(request.form.get('monto_pagado', 0))
                if monto_pagado <= 0:
                    return jsonify({"error": "Debe ingresar un monto pagado mayor a cero."}), 400
                if monto_pagado < total_final:
                    return jsonify({"error": "El monto pagado es insuficiente para cubrir el total de la factura."}), 400
                    
                cambio = monto_pagado - total_final

                # Crear la factura usando el método del modelo
                nueva_factura = Factura.crear_factura(
                    clientes_idclientes,
                    vendedores_idvendedores,
                    datetime.today().date(),
                    datetime.today().time(),
                    total_final,
                    impuesto,
                    descuento,
                    monto_pagado,
                    cambio,
                    
                )

                if not nueva_factura:
                    return jsonify({"error": "Error al crear la factura."}), 500
                

                # Agregar detalles de los productos
                if not DetalleProducto.agregar_detalles(nueva_factura['id'], productos):
                    return jsonify({"error": "Error al agregar productos a la factura."}), 500
                    

                return jsonify({
                    "success": True,
                    "message": "Factura creada exitosamente",
                    "cambio": cambio
                }), 200

            except Exception as e:
                return jsonify({"error": f"Error al crear la factura: {str(e)}"}), 500

          
        # GET: Cargar datos para el formulario
        try:
            # Obtener el usuario logueado
            usuario_id = session.get('usuario_id')

            vendedor_actual = Vendedores.obtener_vendedor_por_usuario(usuario_id)
            
            if not vendedor_actual:
                error_message = "No se encontró un vendedor asociado al usuario actual."
                return render_template('form_error.html', error=error_message), 400

            
            productos = Productos.obtener_productos()
            return render_template('form_generacion_factura.html', vendedor_actual=vendedor_actual, productos=productos, titulo_pagina="Generar factura")
           
        except Exception as e:
            error_message = f"Error al cargar los datos: {str(e)}"
            return render_template('form_error.html', error=error_message,titulo_pagina="vendedor no asociado"), 500
        
    #--------------------------

    #Ruta para consultar las facturas
    @app.route('/facturas_por_fecha', methods=['GET'])
    @role_required(['administrador','vendedor'])
    def obtener_facturas_por_fecha():
        fecha = request.args.get('fecha')  # Obtener la fecha de los parámetros de la URL
        
        # Llamar al método en el modelo para buscar facturas por la fecha
        facturas_data = Factura.buscar_por_fecha(fecha)
        
        if facturas_data:
            return jsonify(facturas_data), 200
        else:
            return jsonify({'message': 'No se encontraron facturas para la fecha seleccionada'}), 404
    
    #---------------

    #Ruta para ver el detalle de las facturas
    @app.route('/detalles_factura/<int:id_factura>', methods=['GET'])
    @role_required(['administrador','vendedor'])
    def obtener_detalles_factura(id_factura):
        # Llamar al método en el modelo para obtener los detalles de la factura
        factura_data = Factura.obtener_detalles(id_factura)

        if factura_data:
            return jsonify(factura_data), 200
        else:
            return jsonify({'message': 'Factura no encontrada'}), 404
    
    #-----------------

   