//scripts actualizar el vendedor
$(document).ready(function () {
    $('#formEditarVendedor').on('submit', function (event) {
        event.preventDefault(); // Evitar el envío estándar del formulario

        // Serializar datos del formulario
        var formData = $(this).serialize();

        // Enviar datos al backend con AJAX
        $.ajax({
            type: 'POST',
            url: '/vendedores_actualizar',
            data: formData,
            dataType: 'json', // Especifica que el backend responde en JSON
            success: function (response) {
                alert(response.message); // Mensaje de éxito
                window.location.href = '/vendedores_ver';
            },

            error: function (xhr) {
                const errores = xhr.responseJSON ? xhr.responseJSON.errores : {};

                // Limpiar mensajes de error previos
                $('#nombreVendedorError').text('');
                $('#numeroDocumentoError').text('');
                $('#telefonoVendedorError').text('');
                $('#direccionVendedorError').text('');
                $('#emailVendedorError').text('');
                $('#mensajeErrorGeneral').text('');

                // Mostrar mensajes de error específicos
                if (errores.nombrevendedor) {
                    $('#nombreVendedorError').text(errores.nombreVendedor);
                }
                if (errores.numeroDocumento) {
                    $('#numeroDocumentoError').text(errores.numeroDocumento);
                }
                if (errores.telefonoVendedor) {
                    $('#telefonoVendedorError').text(errores.telefonoVendedor);
                }
                if (errores.direccionVendedor) {
                    $('#direccionVendedorError').text(errores.direccionVendedor);
                }
                if (errores.emailVendedor) {
                    $('#emailVendedorError').text(errores.emailVendedor);
                }

                // Mostrar mensaje de error general si existen errores
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

//scripts elimiar vendedor 
$(document).ready(function () {
    $('#eliminarVendedorForm').on('submit', function (event) {
        event.preventDefault(); // Evitar el envío estándar del formulario

        // Solicitar confirmación al usuario
        if (!confirm("¿Estás seguro de que deseas eliminar este vendedor? Esta acción no se puede deshacer.")) {
            // Si el usuario cancela, no hace nada
            return;
        }

        // Serializar datos del formulario
        var formData = $(this).serialize();

        // Limpiar mensajes de error previos
        $('#eliminarvendedorMensaje').empty();

        // Enviar datos al backend con AJAX
        $.ajax({
            type: 'POST',
            url: '/vendedores_eliminar',
            data: formData,
            dataType: 'json',
            success: function (response) {
                // Mostrar mensaje de éxito
                $('#eliminarvendedorMensaje').html(`<p class="text-success">${response.message}</p>`);

                // Opcional: redirigir después de eliminar para actualizar la lista de vendedores
                setTimeout(function () {
                    window.location.href = '/vendedores_ver'; // Redirige a la lista de vendedores
                }, 1500);
            },
            error: function (xhr) {
                const errores = xhr.responseJSON ? xhr.responseJSON.errores : {};

                // Mostrar mensajes de error específicos
                if (errores.idvendedores) {
                    $('#eliminarvendedorMensaje').append(`<p class="text-danger">${errores.idvendedores}</p>`);
                }
                
                // Mostrar mensaje de error general si no hay errores específicos
                if (Object.keys(errores).length === 0 && xhr.responseJSON && xhr.responseJSON.message) {
                    $('#eliminarvendedorMensaje').html(`<p class="text-danger">${xhr.responseJSON.message}</p>`);
                } else if (Object.keys(errores).length === 0) {
                    $('#eliminarvendedorMensaje').html('<p class="text-danger">Ocurrió un error inesperado. Inténtalo nuevamente.</p>');
                }
            }
        });
    });
});
