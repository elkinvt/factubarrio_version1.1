//Búsqueda de Cliente 
$('#buscarDocumento').on('input', function () {
    var query = $(this).val();

    if (query.length >=5 && query.length <=15 && /^[0-9]+$/.test(query)) {
        $.ajax({
            type: "GET",
            url: "/buscar_clientes_por_numero_documento?q=" + query,
            dataType: 'json',
            success: function (data) {
                mostrarSugerenciasClientes(data);
            },
            error: function (xhr) {
                // Manejar errores según el código de estado
                if (xhr.status === 400 ) {
                    var response = JSON.parse(xhr.responseText);
                    $('#listaSugerenciasClientes').html('<div class="list-group-item">' + response.error + '</div>');
                } else if (xhr.status === 403){
                    var response = JSON.parse(xhr.responseText);
                    $('#listaSugerenciasClientes').html('<div class="list-group-item">' + response.message + '</div>');
                } else if (xhr.status === 404) {
                    $('#listaSugerenciasClientes').html('<div class="list-group-item">No se encontraron clientes.</div>');
                } else {
                    $('#listaSugerenciasClientes').html('<div class="list-group-item">Ocurrió un error inesperado.</div>');
                }
                
            }
        });
    } else {
        $('#listaSugerenciasClientes').html('');
    }
});

function mostrarSugerenciasClientes(clientes) {
    var listaSugerencias = $('#listaSugerenciasClientes');
    listaSugerencias.html('');

    if (clientes.length > 0) {
        clientes.forEach(function (cliente) {
            var itemText = cliente.numero_documento + ' - ' + cliente.nombre;

            var item = cliente.is_active
                ? $('<div class="list-group-item list-group-item-action"></div>').text(itemText)
                : $('<div class="list-group-item list-group-item-warning"></div>').text(itemText + ' (Inactivo)');

            item.on('click', function () {
                $('#buscarDocumento').val(cliente.numero_documento);
                $('#nombreCliente').val(cliente.nombre);
                $('#numeroDocumentoCliente').val(cliente.numero_documento);
                $('#direccionCliente').val(cliente.direccion);
                $('#telefonoCliente').val(cliente.telefono);
                $('#clienteId').val(cliente.id);
                listaSugerencias.html('');
            });

            listaSugerencias.append(item);
        });
    } else {
        listaSugerencias.html('<div class="list-group-item">No se encontraron clientes.</div>');
    }
}
//termina la busqueda del cliente

//Búsqueda de Producto 
$('#buscarProducto').on('input', function () {
    var query = $(this).val().trim();

    if (query.length > 2) {
        $.ajax({
            type: "GET",
            url: "/buscar_productos?q=" + query,
            dataType: 'json',
            success: function (data) {
                mostrarSugerenciasProducto(data);
            },
            error: function () {
                $('#listaSugerenciasProducto').html('<div class="list-group-item">No se encontraron productos.</div>');
            }
        });
    } else {
        $('#listaSugerenciasProducto').html('');
    }
});

function mostrarSugerenciasProducto(productos) {
    var listaSugerenciasProducto = $('#listaSugerenciasProducto');
    listaSugerenciasProducto.html('');

    if (productos.length > 0) {
        productos.forEach(function (producto) {
            var item = $('<div class="list-group-item list-group-item-action"></div>').text(
                `${producto.nombre} - ${producto.descripcion} - $${producto.precio_unitario}`
            );

            item.on('click', function () {
                $('#buscarProducto').val(producto.nombre);
                $('#productoFacturaCodigo').val(producto.codigo);
                listaSugerenciasProducto.html('');
            });

            listaSugerenciasProducto.append(item);
        });
    } else {
        listaSugerenciasProducto.html('<div class="list-group-item">No se encontraron productos.</div>');
    }
}

//termina la busqueda del producto

//Manejo de Productos y Factura 
var factura = [];  // Array para almacenar productos
var totalConImpuesto = 0;  // Variable global para almacenar el total de la factura con impuesto

function agregarProductoAFactura() {
    var productocodigo = $('#productoFacturaCodigo').val();
    var cantidad = $('#cantidadFactura').val();

    if (!productocodigo || !cantidad || isNaN(cantidad) || cantidad <= 0) {
        $('#productoError').text("Seleccione un producto y una cantidad válida.");
        return;
    }

    $.ajax({
        type: "GET",
        url: `/verificar_producto?codigo=${productocodigo}&cantidad=${cantidad}`,
        dataType: 'json',
        success: function (response) {
            if (response.error) {
                $('#productoError').text(response.error);
            } else {
                factura.push({
                    id: response.id,
                    codigo: response.codigo,
                    producto: response.nombre,
                    cantidad: parseInt(cantidad),
                    precio: response.precio_unitario,
                    subtotal: response.precio_unitario * cantidad
                });
                actualizarDetallesFactura();

                // Limpiar campos
                $('#buscarProducto').val('');
                $('#cantidadFactura').val('');
                $('#productoFacturaCodigo').val('');
                $('#productoError').text('');
            }
        },
        error: function () {
            $('#productoError').text("Error al verificar el producto. Intente nuevamente.");
        }
    });
}

function actualizarDetallesFactura() {
    var facturaBody = document.getElementById('facturaBody');
    facturaBody.innerHTML = '';
    var subtotal = 0;

    factura.forEach(function (item, index) {
        let row = `
                <tr>
                    <td>${item.producto}</td>
                    <td>${item.cantidad}</td>
                    <td>${formatCurrency(item.precio)}</td>
                    <td>${formatCurrency(item.subtotal)}</td>
                    <td><button onclick="eliminarProductoDeFactura(${index})" class="btn btn-danger btn-sm">Eliminar</button></td>
                </tr>`;
        facturaBody.innerHTML += row;
        subtotal += item.subtotal;
    });

    var impuesto = subtotal * 0.19;
    totalConImpuesto = subtotal + impuesto;
    $('#facturaSubtotal').text(formatCurrency(subtotal));
    $('#facturaImpuesto').text(formatCurrency(impuesto));
    $('#facturaTotalConImpuesto').text(formatCurrency(totalConImpuesto));
}

function formatCurrency(value) {
    return value.toLocaleString('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 2 });
}

function eliminarProductoDeFactura(index) {
    factura.splice(index, 1);
    actualizarDetallesFactura();
}


//Verificación en Tiempo Real de Stock 
$('#cantidadFactura').on('input', function () {
    var productocodigo = $('#productoFacturaCodigo').val();
    var cantidad = $(this).val();

    if (!productocodigo || !cantidad || isNaN(cantidad) || cantidad <= 0) {
        $('#stockStatus').text('Seleccione un producto y una cantidad válida.');
        return;
    }

    $.ajax({
        type: "GET",
        url: `/verificar_producto?codigo=${productocodigo}&cantidad=${cantidad}`,
        dataType: 'json',
        success: function (response) {
            $('#stockStatus').text(response.error || "Stock suficiente para la cantidad solicitada.");
        },
        error: function () {
            $('#stockStatus').text("Error al verificar el stock. Intente nuevamente.");
        }
    });
});

//Envío del Formulario y Pago de Factura 
$('#formFactura').on('submit', function (event) {
    event.preventDefault();

    // Asegurarse de que `totalConImpuesto` está actualizado
    actualizarDetallesFactura();

    // Verificar si hay productos en la factura y que el total sea mayor que 0
    if (totalConImpuesto <= 0) {
        alert("No hay productos en la factura o el total es inválido. Agregue productos antes de pagar.");
        return;
    }

    // Convertir el array de productos a JSON y asignarlo al campo oculto
    $('#productosFactura').val(JSON.stringify(factura));

    // Solicitar el monto pagado al usuario
    const montoPagado = prompt(`Ingrese el monto con el que va a pagar. El total es de ${totalConImpuesto.toLocaleString('es-CO', { style: 'currency', currency: 'COP' })}:`);
    if (montoPagado === null || montoPagado.trim() === "" || isNaN(montoPagado) || parseFloat(montoPagado) <= 0) {
        alert("Debe ingresar un monto válido.");
        return;
    }

    // Asignar el monto pagado al campo oculto
    $('#montoPagado').val(parseFloat(montoPagado).toFixed(2));

    // Calcular el cambio a devolver
    const cambio = parseFloat(montoPagado) - totalConImpuesto;

    // Mostrar el mensaje con el cambio a devolver
    if (cambio >= 0) {
        alert(`El cambio a devolver es de ${cambio.toLocaleString('es-CO', { style: 'currency', currency: 'COP' })}`);
    } else {
        alert("El monto ingresado es insuficiente para cubrir el total.");
    }

    // Limpiar errores previos
    $('#clienteError').text('');
    $('#vendedorError').text('');
    $('#descuentoError').text('');
    $('#facturaSuccess').text('');
    $('#facturaError').text('');

    // Obtener la URL del formulario
    const actionUrl = $(this).attr('action');

    // Enviar el formulario al backend usando AJAX
    $.ajax({
        type: 'POST',
        url: $('#formFactura').attr('action'),
        data: $(this).serialize(),
        success: function (response) {
            if (response.success) {
                $('#facturaSuccess').text(response.message);
                $('#formFactura')[0].reset();
                factura = [];
                totalConImpuesto = 0;
                actualizarDetallesFactura();
            }
        },
        error: function (xhr) {
            const errors = xhr.responseJSON;
            if (errors) {
                $('#facturaError').text(errors.error || "Ocurrió un error desconocido. Intente de nuevo.");
                $('#clienteError').text(errors.cliente || "");
                $('#vendedorError').text(errors.vendedor || "");
                $('#descuentoError').text(errors.descuento || "");
                $('#productoError').text(errors.productos || "");
            }
        }
    });
});


//</script> Anulación de la Factura 
function anularFactura() {
    if (!confirm("¿Estás seguro de que deseas anular la factura?")) {
        return;
    }

    // Limpia el array de productos en la factura y actualiza los detalles
    factura = [];
    actualizarDetallesFactura();

    // Limpia los campos del formulario
    $('#buscarDocumento').val('');  // Campo de búsqueda del cliente
    $('#clienteId').val('');
    $('#nombreCliente').val('');
    $('#numeroDocumentoCliente').val('');
    $('#direccionCliente').val('');
    $('#telefonoCliente').val('');

    $('#vendedorFactura').val('');  // Selección de vendedor
    $('#buscarProducto').val('');  // Campo de búsqueda de producto
    $('#cantidadFactura').val('');  // Campo de cantidad
    $('#productoFacturaCodigo').val('');  // Código del producto
    $('#descuentoFactura').val('0');  // Descuento

    // Limpia mensajes de error y sugerencias visuales
    $('#listaSugerenciasClientes').html('');
    $('#listaSugerenciasProducto').html('');
    $('#clienteError').text('');
    $('#vendedorError').text('');
    $('#productoError').text('');
    $('#stockStatus').text('');
    $('#facturaSuccess').text('');
    $('#facturaError').text('');

    alert("Factura anulada correctamente.");
}
