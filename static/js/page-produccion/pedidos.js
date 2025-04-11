
function cargarDetallesPedido() {
    document.body.addEventListener('click', function (event) {
        const btnDetalle = event.target.closest('.btn-detalle');
        if (!btnDetalle) return;

        event.preventDefault();

        const pedidoId = btnDetalle.getAttribute('data-pedido-id');
        const modalElement = document.getElementById('modalDetallesPedidos');

        if (!modalElement) {
            console.error('No se encontró el modal modalDetallesPedidos');
            return;
        }

        const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);

        const modalTitle = modalElement.querySelector('.modal-title');
        const modalBody = modalElement.querySelector('.modal-body tbody');

        modalTitle.textContent = `Detalles pedido #${pedidoId}`;
        modalBody.innerHTML = '<tr><td colspan="4" class="text-center">Cargando detalles...</td></tr>';

        fetch(`/detalles-pedido?idPedido=${pedidoId}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => response.json())
            .then(data => {
                modalBody.innerHTML = '';

                if (data.length === 0) {
                    modalBody.innerHTML = '<tr><td colspan="4" class="text-center">No hay detalles disponibles</td></tr>';
                    return;
                }

                data.forEach((detalle, index) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <th scope="row" style="align-content: center;" id="${detalle.id_galleta}">${index + 1}</th>
                        <td style="align-content: center;">${detalle.nombre_galleta}</td>
                        <td style="align-content: center;" name="cantidad">${detalle.cantidad}</td>
                        <td style="align-content: center;" name="tipoPedido">${detalle.tipo_pedido}</td>
                        <td style="align-content: center;" hidden="hidden" name="id_pedido">${detalle.id_pedido}</td>
                    `;
                    modalBody.appendChild(row);
                });

                const btnProcesar = document.getElementById('btnProcesarPedido');
                btnProcesar.setAttribute('value', data[0].id_pedido);

                modal.show();

                setTimeout(() => {
                    const firstFocusable = modalElement.querySelector('button:not([disabled])');
                    if (firstFocusable) firstFocusable.focus();
                }, 100);
            })
            .catch(error => {
                console.error('Error:', error);
                modalBody.innerHTML = '<tr><td colspan="4" class="text-center text-danger">Error al cargar los detalles</td></tr>';
                modal.show();
            });
    });
}
document.addEventListener('DOMContentLoaded', cargarDetallesPedido);

function cargarDetallesPedidoHistorial() {
    document.body.addEventListener('click', function (event) {
        const btnDetalle = event.target.closest('.btn-detalle-historial');
        if (!btnDetalle) return;

        event.preventDefault();

        const pedidoId = btnDetalle.getAttribute('data-pedido-id');
        const modalElement = document.getElementById('modalDetallesPedidosHistorial');

        if (!modalElement) {
            console.error('No se encontró el modal modalDetallesPedidos');
            return;
        }

        const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);

        const modalTitle = modalElement.querySelector('.modal-title');
        const modalBody = modalElement.querySelector('.modal-body tbody');

        modalTitle.textContent = `Detalles pedido #${pedidoId}`;
        modalBody.innerHTML = '<tr><td colspan="4" class="text-center">Cargando detalles...</td></tr>';

        fetch(`/detalles-pedido?idPedido=${pedidoId}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => response.json())
            .then(data => {
                modalBody.innerHTML = '';

                if (data.length === 0) {
                    modalBody.innerHTML = '<tr><td colspan="4" class="text-center">No hay detalles disponibles</td></tr>';
                    return;
                }

                data.forEach((detalle, index) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <th scope="row" style="align-content: center;" id="${detalle.id_galleta}">${index + 1}</th>
                        <td style="align-content: center;">${detalle.nombre_galleta}</td>
                        <td style="align-content: center;" name="cantidad">${detalle.cantidad}</td>
                        <td style="align-content: center;" name="tipoPedido">${detalle.tipo_pedido}</td>
                    `;
                    modalBody.appendChild(row);
                });

                modal.show();

                setTimeout(() => {
                    const firstFocusable = modalElement.querySelector('button:not([disabled])');
                    if (firstFocusable) firstFocusable.focus();
                }, 100);
            })
            .catch(error => {
                console.error('Error:', error);
                modalBody.innerHTML = '<tr><td colspan="4" class="text-center text-danger">Error al cargar los detalles</td></tr>';
                modal.show();
            });
    });
}
document.addEventListener('DOMContentLoaded', cargarDetallesPedidoHistorial);

document.getElementById('btnProcesarPedido').addEventListener('click', function() {
    const filas = document.querySelectorAll('#tblDetalleProduccion tbody tr');
    const datosGalletas = [];

    filas.forEach(fila => {
        const th = fila.querySelector('th');
        const idGalleta = th ? th.id : null;

        const tdCantidad = fila.querySelector('td[name="cantidad"]');
        const cantidad = tdCantidad ? parseInt(tdCantidad.textContent) : 0;
        const tdIdPedido = fila.querySelector('td[name="id_pedido"]');
        const id_pedido = tdIdPedido ? tdIdPedido.textContent.trim() : '';
        const tdTipoPedido = fila.querySelector('td[name="tipoPedido"]');
        const tipoPedido = tdTipoPedido ? tdTipoPedido.textContent.trim() : '';
        
        if (idGalleta && !isNaN(cantidad)) {
            datosGalletas.push({
                id_galleta: idGalleta,
                cantidad: cantidad,
                tipo_pedido: tipoPedido,
                id_pedido: id_pedido
            });
        }
    });
    
    enviarAlServicio(datosGalletas);
});

function enviarAlServicio(datos) {
    console.log(datos)
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;
    
    fetch('/procesar-pedido', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken 
        },
        body: JSON.stringify({ 
            lst_detalles: datos
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success)
            alert(data.message)
            window.location = '/cocina-pedidos'
        if (data.error)
            alert(data.message)
    });
}

function actualizarTituloHistorialPedidos() {
    const fechaSeleccionada = document.getElementById('inpFecha').value;
    const tituloHistorial = document.getElementById('tituloHistorial');

    if (fechaSeleccionada) {
        const [anio, mes, dia] = fechaSeleccionada.split('-');
        const fechaFormateada = `${dia}/${mes}/${anio}`;
        tituloHistorial.textContent = `Historial Pedidos - ${fechaFormateada}`;
    } else {
        tituloHistorial.textContent = 'Historial Pedidos';
    }

    document.getElementById("formHistorialPedidos").submit()
}