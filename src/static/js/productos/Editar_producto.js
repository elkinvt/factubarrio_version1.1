//scripts actualizar el producto
$(document).ready(function () {
    $('#formEditarProducto').on('submit', function (event) {
        event.preventDefault(); // Evita el envío tradicional del formulario

        // Serializar los datos del formulario
        var formData = $(this).serialize();

        // Obtener la URL de acción del formulario
        var actionUrl = $(this).attr('action');

        // Enviar datos con AJAX
        $.ajax({
            type: 'POST',
            url: actionUrl, 
            data: formData,
            dataType: 'json',
            success: function (response) {
                if (response.success) {
                    alert(response.message); // Mensaje de éxito
                    window.location.href = '/productos_ver'; // Redirige a la lista de productos
                }
            },
            error: function (xhr) {
                // Limpiar mensajes de error previos
                $('#codigoProductoError').text('');
                $('#nombreProductoError').text('');
                $('#descripcionProductoError').text('');
                $('#categoriaProductoError').text('');
                $('#precioProductoError').text('');
                $('#unidadMedidaProductoError').text('');
                $('#presentacionProductoError').text('');
                $('#cantidadStockProductoError').text('');
                $('#mensajeErrorGeneral').text('');

                console.log(xhr.responseJSON); // Esto imprimirá los errores en la consola


                // Procesar errores específicos y mostrar mensajes en el HTML
                const errores = xhr.responseJSON ? xhr.responseJSON.errors : {};

                // Mostrar mensajes de error específicos
                if (errores.codigo) {
                    $('#codigoProductoError').text(errores.codigo);
                }
                if (errores.nombre) {
                    $('#nombreProductoError').text(errores.nombre);
                }
                if (errores.descripcion) {
                    $('#descripcionProductoError').text(errores.descripcion);
                }
                if (errores.categoria_id) {
                    $('#categoriaProductoError').text(errores.categoria_id);
                }
                if (errores.precio) {
                    $('#precioProductoError').text(errores.precio);
                }
                if (errores.unidadMedidaProducto) {
                    $('#unidadMedidaProductoError').text(errores.unidadMedidaProducto);
                }
                if (errores.presentacion) {
                    $('#presentacionProductoError').text(errores.presentacion);
                }
                if (errores.cantidad_stock) {
                    $('#cantidadStockProductoError').text(errores.cantidad_stock);
                }

                // Mostrar mensaje de error general si existen otros errores
                if (Object.keys(errores).length > 0) {
                    $('#mensajeErrorGeneral').text("Corrige los errores en el formulario antes de guardar.");
                } else if (xhr.responseJSON && xhr.responseJSON.message) {
                    $('#mensajeErrorGeneral').text(xhr.responseJSON.message);
                } else {
                    $('#mensajeErrorGeneral').text('Ocurrió un error inesperado. Inténtalo nuevamente.');
                }
            }
        });
    });
});

//scripts cambio de estado 
$(document).ready(function () {
    $('#toggleEstadoProductoForm').on('submit', function (event) {
        event.preventDefault(); // Evitar la recarga de la página

        // Obtener el formulario y sus datos
        const form = $(this);
        const formData = form.serialize(); // Serializar los datos del formulario

        // Limpiar mensajes previos
        $('#toggleEstadoProductoMensaje').html('');

        $.ajax({
            type: 'POST', // Método HTTP
            url: '/productos_toggle_estado', // URL de la ruta en Flask
            data: formData, // Datos del formulario
            dataType: 'json', // Esperar respuesta JSON
            success: function (response) {
                if (response.success) {
                    // Mostrar mensaje de éxito
                    $('#toggleEstadoProductoMensaje').html(
                        `<p class="text-success">${response.message}</p>`
                    );

                    // Cambiar el texto del botón según el nuevo estado
                    const button = form.find('button');
                    if (button.text().trim() === 'Desactivar Producto') {
                        button.text('Activar Producto');
                    } else {
                        button.text('Desactivar Producto');
                    }
                } else {
                    // Mostrar mensaje de error
                    $('#toggleEstadoProductoMensaje').html(
                        `<p class="text-success"">${response.message}</p>`
                    );
                }
            },
            error: function (xhr) {
                if (xhr.status === 400) {
                    // Mostrar errores de validación
                    const errores = xhr.responseJSON.errores;
                    let mensajeErrores = '<p class="text-success""><ul>';
                    for (const campo in errores) {
                        mensajeErrores += `<li>${errores[campo]}</li>`;
                    }
                    mensajeErrores += '</ul></p>';
                    $('#toggleEstadoProductoMensaje').html(mensajeErrores);
                } else {
                    // Mostrar error general
                    $('#toggleEstadoProductoMensaje').html(
                        `<p class="text-success"">Ocurrió un error inesperado. Inténtalo de nuevo.</p>`
                    );
                }
            }
        });
    });
});

//scripts de elimiar 
$(document).ready(function () {
    $('#eliminarProductoForm').on('submit', function (event) {
        event.preventDefault(); // Evitar la recarga de la página

        // Solicitar confirmación al usuario
        if (!confirm("¿Estás seguro de que deseas eliminar este producto? Esta acción no se puede deshacer.")) {
            // Si el usuario cancela, no hace nada
            return;
        }

        // Obtener el formulario y sus datos
        const form = $(this);
        const formData = form.serialize(); // Serializar los datos del formulario

        // Limpiar mensajes previos
        $('#eliminarProductoMensaje').html('');

        // Enviar datos al backend con AJAX
        $.ajax({
            type: 'POST', // Método HTTP
            url: '/productos_eliminar', // URL de la ruta en Flask
            data: formData, // Datos del formulario
            dataType: 'json', // Esperar respuesta JSON
            success: function (response) {
                if (response.success) {
                    // Mostrar mensaje de éxito
                    $('#eliminarProductoMensaje').html(
                        `<p class="text-success"">${response.message}</p>`
                    );

                    // Redirigir después de un tiempo si es necesario
                    setTimeout(function () {
                        window.location.href = '/productos_ver'; // Redirige a la lista de productos
                    }, 1500);
                } else {
                    // Mostrar mensaje de error
                    $('#eliminarProductoMensaje').html(
                        `<p class="text-success"">${response.message}</p>`
                    );
                }
            },
            error: function (xhr) {
                if (xhr.status === 400) {
                    // Mostrar errores de validación
                    const errores = xhr.responseJSON.errores;
                    let mensajeErrores = '<p class="text-success""><ul>';
                    for (const campo in errores) {
                        mensajeErrores += `<li>${errores[campo]}</li>`;
                    }
                    mensajeErrores += '</ul></p>';
                    $('#eliminarProductoMensaje').html(mensajeErrores);
                } else {
                    // Mostrar error general
                    $('#eliminarProductoMensaje').html(
                        `<p class="text-success"">Ocurrió un error inesperado. Inténtalo de nuevo.</p>`
                    );
                }
            }
        });
    });
});
