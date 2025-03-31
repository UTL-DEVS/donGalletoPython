function confirmarCancelacion(ventaId) {
    const form = document.getElementById('formCancelarVenta');
    form.action = `/eliminar_venta/${ventaId}`;
    
    document.getElementById('ventaDetalles').innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
            <p>Cargando detalles...</p>
        </div>`;
    
    fetch(`/api/venta/${ventaId}`)
        .then(response => {
            if (!response.ok) throw new Error('Error en la respuesta');
            return response.json();
        })
        .then(data => {
            let detallesHTML = `
                <p><strong>ID Venta:</strong> ${data.id}</p>
                <p><strong>Total:</strong> $${data.total.toFixed(2)}</p>
                <p><strong>Fecha:</strong> ${new Date(data.fecha).toLocaleString()}</p>
                <p><strong>Estado:</strong> ${data.estado}</p>
                <hr>
                <h6>Detalles:</h6>
                <ul class="list-group">`;
            
            data.detalles.forEach(detalle => {
                detallesHTML += `
                    <li class="list-group-item">
                        ${detalle.galleta_nombre} - 
                        ${detalle.cantidad} x $${detalle.precio_unitario.toFixed(2)} = 
                        $${detalle.subtotal.toFixed(2)} (${detalle.tipo_venta})
                    </li>`;
            });
            
            detallesHTML += `</ul>`;
            document.getElementById('ventaDetalles').innerHTML = detallesHTML;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('ventaDetalles').innerHTML = `
                <div class="alert alert-danger">
                    Error al cargar detalles: ${error.message}
                </div>`;
        });
}

document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    const form = document.getElementById('formCancelarVenta');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        fetch(form.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: new URLSearchParams(new FormData(form))
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al procesar la solicitud');
        });
    });
});