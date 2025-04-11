document.addEventListener('DOMContentLoaded', function() {
    const btnCarrito = document.getElementById('btn-carrito');
    const overlay = document.getElementById('overlay');
    const carritoElement = document.getElementById('carrito');
    
    if (btnCarrito && overlay && carritoElement) {
        btnCarrito.addEventListener('click', toggleCarrito);
        overlay.addEventListener('click', toggleCarrito);
    }
    
    function toggleCarrito() {
        carritoElement.classList.toggle('mostrar');
        overlay.classList.toggle('mostrar');
        document.body.style.overflow = carritoElement.classList.contains('mostrar') ? 'hidden' : '';
    }
    
    document.querySelectorAll('input[name="peso"]').forEach(input => {
        input.addEventListener('input', function() {
            const galletaId = this.id.split('-')[1];
            const unidadesSpan = document.getElementById(`unidades-${galletaId}`);
            const peso = parseInt(this.value) || 0;
            
            if (peso < 10) {
                this.value = 10;
                unidadesSpan.textContent = '1';
            } else {
                unidadesSpan.textContent = Math.floor(peso / 10);
            }
        });
    });
    
    const selectGalleta = document.getElementById('galleta-paquete');
    if (selectGalleta) {
        selectGalleta.addEventListener('change', function() {
            const option = this.options[this.selectedIndex];
            if (option && option.dataset.galletaPrecio) {
                const precio = parseFloat(option.dataset.galletaPrecio);
                document.getElementById('precio-1kg').textContent = (precio * 100).toFixed(2);
                document.getElementById('precio-700g').textContent = (precio * 70).toFixed(2);
                document.getElementById('precio-500g').textContent = (precio * 50).toFixed(2);
            }
        });
    }
    
    const btnPedidos = document.getElementById('btn-pedidos');
    if (btnPedidos) {
        btnPedidos.addEventListener('click', function() {
            const modalElement = document.getElementById('pedidosModal');
            modalElement.removeAttribute('aria-hidden');
            
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
            
            cargarPedidosCompletados();
        });
    }
    
    function cargarPedidosCompletados() {
        fetch('/obtener_pedidos_completados', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error || `HTTP error! status: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            if (!Array.isArray(data)) {
                if (data.error) {
                    throw new Error(data.error);
                }
                throw new Error('Respuesta inesperada del servidor');
            }
            
            const tbody = document.querySelector('#tablaPedidos tbody');
            tbody.innerHTML = '';
            
            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" class="text-center">No hay pedidos completados</td></tr>';
                return;
            }
            
            data.forEach(pedido => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${pedido.id_pedido || 'N/A'}</td>
                    <td>${pedido.usuario || 'Anónimo'}</td>
                    <td>${pedido.fecha_pedido || 'N/A'}</td>
                    <td>$${(pedido.total || 0).toFixed(2)}</td>
                    <td>
                        <button class="btn btn-sm btn-primary btn-cargar-pedido" data-id="${pedido.id_pedido}">
                            <i class="fas fa-cart-plus"></i> Cargar al carrito
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });    
            
            document.querySelectorAll('.btn-cargar-pedido').forEach(btn => {
                btn.addEventListener('click', function() {
                    const idPedido = this.getAttribute('data-id');
                    cargarPedidoAlCarrito(idPedido);
                });
            });
        })
        .catch(error => {
            console.error('Error al cargar pedidos:', error);
            iziToast.error({
                title: 'Error',
                message: error.message || 'No se pudieron cargar los pedidos',
                position: 'topRight'
            });
        });
    }
    
    function cargarPedidoAlCarrito(idPedido) {
        fetch(`/cargar_pedido/${idPedido}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error || `HTTP error! status: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                iziToast.success({
                    title: 'Éxito',
                    message: 'Pedido cargado al carrito',
                    position: 'topRight'
                });
                
                window.location.reload();
                
                const modal = bootstrap.Modal.getInstance(document.getElementById('pedidosModal'));
                modal.hide();
            } else {
                iziToast.error({
                    title: 'Error',
                    message: data.error || 'Error al cargar el pedido',
                    position: 'topRight'
                });
            }
        })
        .catch(error => {
            console.error('Error al cargar pedido:', error);
            iziToast.error({
                title: 'Error',
                message: error.message || 'Error al cargar el pedido',
                position: 'topRight'
            });
        });
    }

    const formProcesarVenta = document.getElementById('form-procesar-venta');
    if (formProcesarVenta) {
        formProcesarVenta.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const btn = document.getElementById('btn-procesar-venta');
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Procesando...';
            
            fetch(this.action, {
                method: 'POST',
                body: new FormData(this),
                headers: {
                    'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
                }
            })
            .then(response => {
                if (response.ok && response.headers.get('content-type')?.includes('application/pdf')) {
                    return response.blob().then(blob => {
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `ticket_venta_${new Date().getTime()}.pdf`;
                        document.body.appendChild(a);
                        a.click();
                        a.remove();
                        window.URL.revokeObjectURL(url);
                        
                        showFlashMessage('Venta realizada correctamente', 'success');
                        
                        setTimeout(() => {
                            window.location.reload();
                        }, 2000);
                    });
                } else if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    return response.text().then(text => {
                        throw new Error(text || 'Error desconocido');
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showFlashMessage('Error al procesar la venta: ' + error.message, 'danger');
            })
            .finally(() => {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-cash-register me-2"></i> Procesar Venta';
            });
        });
    }
    
    function showFlashMessage(message, category) {
        const toastType = 
            category === 'success' ? 'success' :
            category === 'danger' ? 'error' :
            category === 'warning' ? 'warning' : 'info';
        
        const title = 
            category === 'success' ? 'Éxito' :
            category === 'danger' ? 'Error' :
            category === 'warning' ? 'Advertencia' : 'Información';
        
        iziToast[toastType]({
            title: title,
            message: message,
            position: 'topRight',
            timeout: 5000,
            progressBar: true,
            closeOnClick: true,
            displayMode: 2
        });
    }
});