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
});

document.getElementById('form-procesar-venta').addEventListener('submit', function(e) {
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
                
                window.location.reload();
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
        alert('Error al procesar la venta: ' + error.message);
    })
    .finally(() => {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-cash-register me-2"></i> Procesar Venta';
    });
});