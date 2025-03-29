document.addEventListener('DOMContentLoaded', function() {
    const carritoElement = document.getElementById('carrito');
    const btnCarrito = document.getElementById('btn-carrito');
    const overlay = document.getElementById('overlay');
    const contadorCarrito = document.getElementById('contador-carrito');
    
    btnCarrito.addEventListener('click', () => {
        carritoElement.classList.toggle('mostrar');
        overlay.classList.toggle('mostrar');
    });
    
    overlay.addEventListener('click', () => {
        carritoElement.classList.remove('mostrar');
        overlay.classList.remove('mostrar');
    });
    
    document.querySelectorAll('.formulario-agregar').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const productoId = this.dataset.productoId;
            const productoNombre = this.dataset.productoNombre;
            const productoPrecio = parseFloat(this.dataset.productoPrecio);
            const stock = parseInt(this.dataset.stock);
            const cantidad = parseInt(this.querySelector('input[name="cantidad"]').value) || 1;
            
            if (cantidad > stock) {
                alert('No hay suficiente stock disponible');
                return;
            }
            
            fetch('/api/agregar_carrito', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    producto_id: productoId,
                    producto_nombre: productoNombre,
                    precio: productoPrecio,
                    cantidad: cantidad
                })
            })
            .then(respuesta => respuesta.json())
            .then(datos => {
                if (datos.exito) {
                    contadorCarrito.textContent = datos.carrito.length;
                    window.location.reload();
                } else {
                    alert(datos.error || 'Error al agregar al carrito');
                }
            });
        });
    });
    
    document.querySelectorAll('.remover-item').forEach(btn => {
        btn.addEventListener('click', function() {
            const productoId = this.dataset.productoId;
            
            fetch(`/api/eliminar_del_carrito/${productoId}`, {
                method: 'DELETE'
            })
            .then(respuesta => respuesta.json())
            .then(datos => {
                if (datos.exito) {
                    contadorCarrito.textContent = datos.carrito.length;
                    window.location.reload();
                }
            });
        });
    });
    
    document.getElementById('vaciar-carrito').addEventListener('click', function() {
        if (confirm('¿Estás seguro de vaciar el carrito?')) {
            fetch('/api/vaciar_carrito', {
                method: 'POST'
            })
            .then(respuesta => respuesta.json())
            .then(datos => {
                if (datos.exito) {
                    contadorCarrito.textContent = '0';
                    window.location.reload();
                }
            });
        }
    });
    
    document.getElementById('procesar-venta').addEventListener('click', function() {
        if (confirm('¿Confirmar compra?')) {
            fetch('/api/procesar_venta', {
                method: 'POST'
            })
            .then(respuesta => respuesta.json())
            .then(datos => {
                if (datos.exito) {
                    alert(datos.mensaje);
                    contadorCarrito.textContent = '0';
                    if (datos.url_ticket) {
                        window.location.href = datos.url_ticket;
                    }
                } else {
                    alert(datos.error || 'Error al procesar la venta');
                }
            });
        }
    });
});

function validarCantidad(input) {
    if (input.value < 1) {
        input.setCustomValidity('La cantidad debe ser al menos 1');
    } else if (input.value > parseInt(input.max)) {
        input.setCustomValidity('No hay suficiente stock');
    } else {
        input.setCustomValidity('');
    }
}