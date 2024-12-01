//scripts actualizar el usuario
$(document).ready(function () {
    $('#formEditarusuario').on('submit', function (event) {
        event.preventDefault(); // Evitar el envío estándar del formulario

        // Serializar datos del formulario
        var formData = $(this).serialize();

        // Enviar datos al backend con AJAX
        $.ajax({
            type: 'POST',
            url: '/usuarios_actualizar',
            data: formData,
            dataType: 'json', // Especifica que el backend responde en JSON
            success: function (response) {
                alert(response.message); // Mensaje de éxito
                window.location.href = '/usuarios_ver'; // Redirigir al listado de usuarios
            },

            error: function (xhr) {
                const errores = xhr.responseJSON ? xhr.responseJSON.errores : {};

                // Limpiar mensajes de error previos
                $('#nombreUsuarioError').text('');
                $('#emailUsuarioError').text('');
                $('#nuevaContraseñaError').text('');
                $('#confirmarContraseñaError').text('');
                $('#rolUsuarioError').text('');
                $('#mensajeErrorGeneral').text('');

                // Mostrar mensajes de error específicos
                if (errores.nombreUsuario) {
                    $('#nombreUsuarioError').text(errores.nombreUsuario);
                }
                if (errores.emailUsuario) {
                    $('#emailUsuarioError').text(errores.emailUsuario);
                }
                if (errores.nuevaContraseña) {
                    $('#nuevaContraseñaError').text(errores.nuevaContraseña);
                }
                if (errores.confirmarContraseña) {
                    $('#confirmarContraseñaError').text(errores.confirmarContraseña);
                }
                if (errores.rolUsuario) {
                    $('#rolUsuarioError').text(errores.rolUsuario);
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


// AJAX para verificar el email en tiempo real
function verificarEmail(email) {
    fetch(`/usuarios/verificar_email?email=${email}`)
        .then(response => response.json())
        .then(data => {
            const emailError = document.getElementById('emailUsuarioError');
            if (data.exists) {
                emailError.textContent = "Este email ya está en uso.";
            } else {
                emailError.textContent = "";
            }
        })
        .catch(error => {
            console.error('Error al verificar el email:', error);
        });
}

//scripts cambio de estado 
$(document).ready(function () {
    $('#toggleEstadoUsuarioForm').on('submit', function (event) {
        event.preventDefault(); // Evitar el envío estándar del formulario

        // Serializar datos del formulario
        var formData = $(this).serialize();
        //console.log(formData);


        // Limpiar mensajes de error previos
        $('#toggleEstadoUsuarioMensaje').empty();

        // Enviar datos al backend con AJAX
        $.ajax({
            type: 'POST',
            url: '/usuario_toggle_estado',
            data: formData,
            dataType: 'json',
            success: function (response) {
                // Mostrar mensaje de éxito
                $('#toggleEstadoUsuarioMensaje').html(`<p class="text-success">${response.message}</p>`);

                // Cambiar el texto del botón dinámicamente
                const button = $('#toggleEstadoUsuarioForm button');
                if (button.text().includes('Activar')) {
                    button.text('Desactivar usuario');
                } else {
                    button.text('Activar usuario');
                }
            },
            error: function (xhr) {
                const response = xhr.responseJSON; // Extraer la respuesta del servidor
                const errores = xhr.responseJSON ? xhr.responseJSON.errores : {};

                // Mostrar mensajes de error específicos
                if (errores && errores.id_usuario) {
                    // Mostrar mensaje de error específico para id_usuario
                    $('#toggleEstadoUsuarioMensaje').append(`<p class="text-danger">${errores.id_usuario}</p>`);
                }

                // Mostrar mensaje general de error si no hay errores específicos
                    if (response && response.message) {
                        $('#toggleEstadoUsuarioMensaje').append(`<p class="text-danger">${response.message}</p>`);
                    } else if (!errores) {
                        $('#toggleEstadoUsuarioMensaje').append('<p class="text-danger">Ocurrió un error inesperado. Inténtalo nuevamente.</p>');
                    }
                }
            
        });
    });
});

//scripts de elimiar 
$(document).ready(function () {
    $('#eliminarUsuarioForm').on('submit', function (event) {
        event.preventDefault(); // Evitar el envío estándar del formulario

        // Solicitar confirmación al usuario
        if (!confirm("¿Estás seguro de que deseas eliminar este usuario? Esta acción no se puede deshacer.")) {
            // Si el usuario cancela, no hace nada
            return;
        }

        // Serializar datos del formulario
        var formData = $(this).serialize();

        // Limpiar mensajes de error previos
        $('#EliminarUsuarioMensaje').empty();

        // Enviar datos al backend con AJAX
        $.ajax({
            type: 'POST',
            url: '/usuario_eliminar',
            data: formData,
            dataType: 'json',
            success: function (response) {
                // Mostrar mensaje de éxito
                $('#EliminarUsuarioMensaje').html(`<p class="text-success">${response.message}</p>`);

                // Opcional: redirigir después de eliminar para actualizar la lista de usuarioss
                setTimeout(function () {
                    window.location.href = '/usuarios_ver'; // Redirige a la lista de usuarios
                }, 1500);
            },
            error: function (xhr) {
                const responseJSON = xhr.responseJSON;
                const errores = responseJSON ? responseJSON.errores : {};

                // Mostrar mensajes de error específicos
                if (errores.id_usuario) {
                    $('#EliminarUsuarioMensaje').append(`<p class="text-danger">${errores.id_usuario}</p>`);
                }
                // Mostrar mensaje de error general
                if (!errores.id_usuario && responseJSON && responseJSON.message) {
                    $('#EliminarUsuarioMensaje').html(`<p class="text-danger">${responseJSON.message}</p>`);
                } else if (!responseJSON) {
                    $('#EliminarUsuarioMensaje').html('<p class="text-danger">Ocurrió un error inesperado. Inténtalo nuevamente.</p>');
                }

            }
        });
    });
});