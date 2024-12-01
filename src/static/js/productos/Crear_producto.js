//JavaScript para manejar el envío con AJAX 

$(document).ready(function () {
    $('#formCrearProducto').on('submit', function (event) {
        event.preventDefault(); // Evitar el envío tradicional del formulario

        // Obtener los datos del formulario
        var formData = $(this).serialize();

        // Enviar datos con AJAX
        $.ajax({
            type: 'POST',
            url: '/productos_crear',
            data: formData,
            dataType: 'json',
            success: function (response) {
                if (response.success) {
                    alert(response.message); // Mensaje de éxito
                    window.location.href = '/productos_ver';
                }
            },
            error: function (xhr) {
                // Procesar errores específicos y mostrar mensajes en el HTML
                const errores = xhr.responseJSON ? xhr.responseJSON.errores : {};

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

                // Mostrar mensajes de error específicos
                if (errores.codigoProducto) {
                    $('#codigoProductoError').text(errores.codigoProducto);
                }
                if (errores.nombreProducto) {
                    $('#nombreProductoError').text(errores.nombreProducto);
                }
                if (errores.descripcionProducto) {
                    $('#descripcionProductoError').text(errores.descripcionProducto);
                }
                if (errores.categoriaProducto) {
                    $('#categoriaProductoError').text(errores.categoriaProducto);
                }
                if (errores.precioProducto) {
                    $('#precioProductoError').text(errores.precioProducto);
                }
                if (errores.unidadMedidaProducto) {
                    $('#unidadMedidaProductoError').text(errores.unidadMedidaProducto);
                }
                if (errores.presentacionProducto) {
                    $('#presentacionProductoError').text(errores.presentacionProducto);
                }
                if (errores.cantidadStockProducto) {
                    $('#cantidadStockProductoError').text(errores.cantidadStockProducto);
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
