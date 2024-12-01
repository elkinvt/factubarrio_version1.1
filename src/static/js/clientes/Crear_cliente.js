//Código JavaScript para manejar el envío con AJAX  en la creacion
$(document).ready(function () {
    $('#formCliente').on('submit', function (event) {
        event.preventDefault(); // Evitar el envío estándar del formulario

        // Serializar datos del formulario
        var formData = $(this).serialize();

        // Enviar datos al backend con AJAX
        $.ajax({
            type: 'POST',
            url: '/clientes_crear',
            data: formData,
            dataType: 'json', // Especifica que el backend responde en JSON
            success: function (response) {
                alert(response.message); // Mensaje de éxito
                window.location.href = '/clientes_ver';
            },
            error: function (xhr) {
                // Procesar errores específicos y mostrar mensajes en el HTML
                const errores = xhr.responseJSON ? xhr.responseJSON.errores : {};

                // Limpiar mensajes de error previos
                $('#tipoDocumentoError').text('');
                $('#numeroDocumentoError').text('');
                $('#nombreClienteError').text('');
                $('#telefonoClienteError').text('');
                $('#direccionClienteError').text('');
                $('#emailClienteError').text('');
                $('#mensajeErrorGeneral').text('');

                // Mostrar mensajes de error específicos
                if (errores.tipoDocumento) {
                    $('#tipoDocumentoError').text(errores.tipoDocumento);
                }
                if (errores.numeroDocumento) {
                    $('#numeroDocumentoError').text(errores.numeroDocumento);
                }
                if (errores.nombreCliente) {
                     $('#nombreClienteError').text(errores.nombreCliente);
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

//Código JavaScript para validacion de datos duplicados(numero_docuemnto, email) del cliente

// Asignar la validación solo a los campos específicos
$('#numeroDocumento').on('blur', function() {
    validarCliente('numeroDocumento');
});

$('#emailCliente').on('blur', function() {
    validarCliente('emailCliente');
});

function validarCliente(campo) {
    // Recopilar los valores de los campos
    const numeroDocumento = $('#numeroDocumento').val().trim();
    const emailCliente = $('#emailCliente').val().trim();

    // Crear un objeto de datos para enviar solo los campos que deben validarse
    const datos = {};
    if (campo === 'numeroDocumento' && numeroDocumento !== '') {
        datos.numeroDocumento = numeroDocumento;
    }
    if (campo === 'emailCliente' && emailCliente !== '') {
        datos.emailCliente = emailCliente;
    }

    // Si no hay datos que validar, salir de la función
    if (Object.keys(datos).length === 0) return;

    // Enviar datos al backend para validación
    $.ajax({
        type: 'POST',
        url: '/validar_cliente',
        contentType: 'application/json',
        data: JSON.stringify(datos),
        success: function(response) {
            // Limpiar mensajes de error para los campos que se están validando
            if (campo === 'numeroDocumento') {
                $('#numeroDocumentoError').text('');
            }
            if (campo === 'emailCliente') {
                $('#emailClienteError').text('');
            }
        },
        error: function(xhr) {
            const errores = xhr.responseJSON.errores || {};
            // Mostrar mensajes de error específicos solo para los campos que se están validando
            if (campo === 'numeroDocumento') {
                $('#numeroDocumentoError').text(errores.numeroDocumento || '');
            }
            if (campo === 'emailCliente') {
                $('#emailClienteError').text(errores.emailCliente || '');
            }
        }
    });
}

