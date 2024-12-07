//Código JavaScript para buscar la factura por fecha
function buscarFacturasPorFecha() {
    let fechaIngresada = $('#fechaConsulta').val();
    let contenedor = $('#listaFacturas');
    contenedor.empty(); // Limpia contenido anterior

    $.ajax({
        url: `/facturas_por_fecha`,
        method: 'GET',
        data: { fecha: fechaIngresada },
        dataType: 'json',
        success: function (data) {
            if (data.length > 0) {
                data.forEach(factura => {
                    contenedor.append(`
                            <tr>
                                <td>${factura.id}</td>
                                <td>${factura.fecha} ${factura.hora}</td>
                                <td>${factura.cliente}</td>
                                <td>$${factura.total.toLocaleString('es-CO', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                                <td><button class="btn btn-info btn-sm" onclick="mostrarDetallesFactura('${factura.id}')">Ver Detalles</button></td>
                            </tr>
                        `);
                });
            } else {
                contenedor.append('<tr><td colspan="5" class="text-center">No se encontraron facturas para la fecha seleccionada.</td></tr>');
            }
        },
        error: function (xhr, status, error) {
            contenedor.append(`<tr><td colspan="5" class="text-center">Error: ${xhr.responseText || 'No se encontraron facturas para la fecha seleccionada.'}</td></tr>`);
        }
    });
}

//Código JavaScript para ver el detalle de la factura
function mostrarDetallesFactura(idFactura) {
    $.ajax({
        url: `/detalles_factura/${idFactura}`,
        method: 'GET',
        dataType: 'json',
        success: function (factura) {
            let fechaFactura = new Date(factura.fecha);
            let horaFactura = factura.hora;

            let detalleHtml = `
                    <p><strong>ID:</strong> ${factura.id}</p>
                    <p><strong>Fecha:</strong> ${factura.fecha} ${factura.hora}</p>
                    <p><strong>Cliente:</strong> ${factura.cliente}</p>
                    <p><strong>Vendedor:</strong> ${factura.vendedor}</p>
                    <p><strong>Impuesto:</strong> $${factura.impuesto.toLocaleString('es-CO', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
                    <p><strong>Total:</strong> $${factura.total.toLocaleString('es-CO', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
                    <p><strong>Monto Pagado:</strong> $${factura.montoPagado.toLocaleString('es-CO', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
                    <p><strong>Cambio:</strong> $${factura.cambio.toLocaleString('es-CO', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
                    <div><strong>Items:</strong></div>
                    <ul>
                        ${factura.items.map(item => `
                            <li>${item.producto} - ${item.cantidad} x $${item.precioUnitario.toLocaleString('es-CO', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            })} = $${item.subtotal.toLocaleString('es-CO', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            })}
                            </li>`).join('')}
                    </ul>
                `;

            $('#detalleFacturaContent').html(detalleHtml);
            let myModal = new bootstrap.Modal(document.getElementById('facturaModal'));
            myModal.show();
        },
        error: function (xhr, status, error) {
            alert(xhr.responseText || 'Detalles de factura no encontrados');
        }
    });
}



