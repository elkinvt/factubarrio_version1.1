//Código JavaScript para manejar el envío con AJAX  en la creacion
$(document).ready(function () {
    $('#crear-usuario-form').on('submit', function (event) {
        event.preventDefault(); // Evita el envío normal del formulario

        // Limpiar mensajes de error previos
        $('#nombreError').text('');
        $('#emailError').text('');
        $('#contraseñaError').text('');
        $('#rolError').text('');
        $('#mensajeErrorGeneral').text('');

        // Serializar datos del formulario
        var formData = $(this).serialize();

        // Obtener la URL de acción del formulario
        var actionUrl = $(this).attr('action');

        $.ajax({
            url: actionUrl,
            method: "POST",
            data: formData,
            dataType: 'json',
            success: function (response) {
                // Redirige o muestra un mensaje de éxito si el usuario fue creado correctamente
                if (response.success) {
                    window.location.href = '/usuarios_ver';
                }
            },
            error: function (xhr) {
                console.log(xhr.responseJSON);

                const errores = xhr.responseJSON ? xhr.responseJSON.errores : {};

                // Mostrar mensajes de error específicos para cada campo
                if (errores.nombre) {
                    $('#nombreError').text(errores.nombre);
                }
                if (errores.email) {
                    $('#emailError').text(errores.email);
                }
                if (errores.contraseña) {
                    $('#contraseñaError').text(errores.contraseña);
                }
                if (errores.rol) {
                    $('#rolError').text(errores.rol);
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
