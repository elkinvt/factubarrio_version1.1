//scripts actualizar el cliente
$(document).ready(function () {
    $('#formEditarCliente').on('submit', function (event) {
        event.preventDefault(); // Evitar el envío estándar del formulario

        // Serializar datos del formulario
        var formData = $(this).serialize();

        // Enviar datos al backend con AJAX
        $.ajax({
            type: 'POST',
            url: '/clientes_actualizar',
            data: formData,
            dataType: 'json', // Especifica que el backend responde en JSON
            success: function (response) {
                alert(response.message); // Mensaje de éxito
                window.location.href = '/clientes_ver';
            },
            error: function (xhr) {
                const errores = xhr.responseJSON ? xhr.responseJSON.errores : {};

                // Limpiar mensajes de error previos
                $('#nombreClienteError').text('');
                $('#numeroDocumentoError').text('');
                $('#telefonoClienteError').text('');
                $('#direccionClienteError').text('');
                $('#emailClienteError').text('');
                $('#mensajeErrorGeneral').text('');

                // Mostrar mensajes de error específicos
                if (errores.nombreCliente) {
                    $('#nombreClienteError').text(errores.nombreCliente);
                }
                if (errores.numeroDocumento) {
                    $('#numeroDocumentoError').text(errores.numeroDocumento);
                }
                if (errores.telefonoCliente) {
                    $('#telefonoClienteError').text(errores.telefonoCliente);
                }
                if (errores.direccionCliente) {
                    $('#direccionClienteError').text(errores.direccionCliente);
                }
                if (errores.emailCliente) {
                    $('#emailClienteError').text(errores.emailCliente);
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

//scripts cambio de estado 
$(document).ready(function () {
    $('#toggleEstadoClienteForm').on('submit', function (event) {
        event.preventDefault(); // Evitar el envío estándar del formulario

        // Serializar datos del formulario
        var formData = $(this).serialize();

        // Limpiar mensajes de error previos
        $('#toggleEstadoClienteMensaje').empty();

        // Enviar datos al backend con AJAX
        $.ajax({
            type: 'POST',
            url: '/clientes_toggle_estado',
            data: formData,
            dataType: 'json',
            success: function (response) {
                // Mostrar mensaje de éxito
                $('#toggleEstadoClienteMensaje').html(`<p class="text-success">${response.message}</p>`);

                // Cambiar el texto del botón dinámicamente
                const button = $('#toggleEstadoClienteForm button');
                if (button.text().includes('Activar')) {
                    button.text('Desactivar cliente');
                } else {
                    button.text('Activar cliente');
                }
            },
            error: function (xhr) {
                const errores = xhr.responseJSON ? xhr.responseJSON.errores : {};

                // Mostrar mensajes de error específicos
                if (errores.idclientes) {
                    $('#toggleEstadoClienteMensaje').append(`<p class="text-danger">${errores.idclientes}</p>`);
                }

                // Mostrar mensaje de error general si no hay errores específicos
                if (Object.keys(errores).length === 0 && xhr.responseJSON && xhr.responseJSON.message) {
                    $('#toggleEstadoClienteMensaje').html(`<p class="text-danger">${xhr.responseJSON.message}</p>`);
                } else if (Object.keys(errores).length === 0) {
                    $('#toggleEstadoClienteMensaje').html('<p class="text-danger">Ocurrió un error inesperado. Inténtalo nuevamente.</p>');
                }
            }
        });
    });
});

//scripts de elimiar 
$(document).ready(function () {
    $('#eliminarClienteForm').on('submit', function (event) {
        event.preventDefault(); // Evitar el envío estándar del formulario

        // Solicitar confirmación al usuario
        if (!confirm("¿Estás seguro de que deseas eliminar este cliente? Esta acción no se puede deshacer.")) {
            // Si el usuario cancela, no hace nada
            return;
        }

        // Serializar datos del formulario
        var formData = $(this).serialize();

        // Limpiar mensajes de error previos
        $('#eliminarClienteMensaje').empty();

        // Enviar datos al backend con AJAX
        $.ajax({
            type: 'POST',
            url: '/clientes_eliminar',
            data: formData,
            dataType: 'json',
            success: function (response) {
                // Mostrar mensaje de éxito
                $('#eliminarClienteMensaje').html(`<p class="text-success">${response.message}</p>`);
                
                // Opcional: redirigir después de eliminar para actualizar la lista de clientes
                setTimeout(function() {
                    window.location.href = '/clientes_ver'; // Redirige a la lista de clientes
                }, 1500);
            },
            error: function (xhr) {
                const errores = xhr.responseJSON ? xhr.responseJSON.errores : {};

                // Mostrar mensajes de error específicos
                if (errores.idclientes) {
                    $('#eliminarClienteMensaje').append(`<p class="text-danger">${errores.idclientes}</p>`);
                }

                // Mostrar mensaje de error general si no hay errores específicos
                if (Object.keys(errores).length === 0 && xhr.responseJSON && xhr.responseJSON.message) {
                    $('#eliminarClienteMensaje').html(`<p class="text-danger">${xhr.responseJSON.message}</p>`);
                } else if (Object.keys(errores).length === 0) {
                    $('#eliminarClienteMensaje').html('<p class="text-danger">Ocurrió un error inesperado. Inténtalo nuevamente.</p>');
                }
            }
        });
    });
});
