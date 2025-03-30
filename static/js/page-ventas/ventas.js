function mostrarNotificacion(mensaje, tipo = 'success') {
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion ${tipo}`;
    notificacion.textContent = mensaje;
    document.body.appendChild(notificacion);
    
    setTimeout(() => notificacion.classList.add('mostrar'), 10);
    setTimeout(() => {
        notificacion.classList.remove('mostrar');
        setTimeout(() => document.body.removeChild(notificacion), 300);
    }, 3000);
}

function calcularPrecioPorPeso(peso, precioUnitario) {
    return (peso / 10) * precioUnitario; 
}

function actualizarVistaCarrito(carrito, total) {
    const carritoLista = document.querySelector('#carrito ul');
    const carritoTotal = document.querySelector('#carrito .text-end strong');
    const contadorCarrito = document.getElementById('contador-carrito');
    
    if (!carritoLista || !carritoTotal || !contadorCarrito) return;
    
    carritoLista.innerHTML = '';
    
    carrito.forEach(item => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        
        let cantidadTexto = '';
        if (item.tipo_venta === 'peso') {
            cantidadTexto = `${item.unidades * 10}g`;
        } else if (item.tipo_venta === 'paquete') {
            cantidadTexto = `${item.unidades} unidades`;
        } else {
            cantidadTexto = `x${item.cantidad}`;
        }
        
        li.innerHTML = `
            ${item.nombre} (${cantidadTexto}) - $${item.subtotal.toFixed(2)}
            <button class="btn btn-danger btn-sm remover-item" 
                data-producto-id="${item.producto_id}"
                data-producto-nombre="${item.nombre}"
                data-tipo-venta="${item.tipo_venta}">
                ❌
            </button>
        `;
        carritoLista.appendChild(li);
    });
    
    carritoTotal.textContent = `Total: $${total.toFixed(2)}`;
    contadorCarrito.textContent = carrito.reduce((sum, item) => sum + (item.tipo_venta === 'unidad' ? item.cantidad : 1), 0);
    
    document.querySelectorAll('.remover-item').forEach(btn => {
        btn.addEventListener('click', removerItemCarrito);
    });
}

async function agregarAlCarrito(item) {
    try {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
        
        const response = await fetch('/api/agregar_carrito', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(item)
        });
        
        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.message || 'Error al agregar al carrito');
        }
        
        const data = await response.json();
        
        if (data.exito) {
            actualizarVistaCarrito(data.carrito, data.nuevo_total);
            mostrarNotificacion(data.mensaje || 'Producto agregado al carrito');
        } else {
            throw new Error(data.error || 'Error en el servidor');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarNotificacion(error.message, 'error');
    }
}

async function removerItemCarrito() {
    try {
        const productoId = this.dataset.productoId;
        const productoNombre = this.dataset.productoNombre;
        const tipoVenta = this.dataset.tipoVenta;
        
        const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
        
        const response = await fetch(`/api/eliminar_del_carrito/${productoId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                producto_nombre: productoNombre,
                tipo_venta: tipoVenta
            })
        });
        
        if (!response.ok) {
            throw new Error('Error al eliminar el producto');
        }
        
        const data = await response.json();
        
        if (data.exito) {
            actualizarVistaCarrito(data.carrito, data.nuevo_total);
            mostrarNotificacion('Producto eliminado del carrito');
            if (data.carrito.length === 0) {
                toggleCarrito();
            }
        } else {
            throw new Error(data.error || 'Error al eliminar');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarNotificacion(error.message, 'error');
    }
}

async function vaciarCarrito() {
    try {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
        
        const response = await fetch('/api/vaciar_carrito', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });
        
        if (!response.ok) {
            throw new Error('Error al vaciar el carrito');
        }
        
        const data = await response.json();
        
        if (data.exito) {
            actualizarVistaCarrito([], 0);
            mostrarNotificacion('Carrito vaciado correctamente');
            toggleCarrito();
        } else {
            throw new Error(data.error || 'Error al vaciar');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarNotificacion(error.message, 'error');
    }
}

function toggleCarrito() {
    const carritoElement = document.getElementById('carrito');
    const overlay = document.getElementById('overlay');
    
    if (!carritoElement || !overlay) return;
    
    const mostrar = !carritoElement.classList.contains('mostrar');
    carritoElement.classList.toggle('mostrar', mostrar);
    overlay.classList.toggle('mostrar', mostrar);
    document.body.style.overflow = mostrar ? 'hidden' : 'auto';
}

function validarPeso(input, stock) {
    const peso = parseInt(input.value);
    const productoId = input.id.split('-')[1];
    const unidadesSpan = document.getElementById(`unidades-${productoId}`);
    
    if (isNaN(peso)) {
        input.value = 10;
        unidadesSpan.textContent = '1';
        return;
    }
    
    const maxPeso = stock * 10;
    if (peso < 10) {
        input.value = 10;
    } else if (peso > maxPeso) {
        input.value = maxPeso;
    }
    
    unidadesSpan.textContent = Math.floor(input.value / 10);
}

function inicializarCarrito() {
    const carritoElement = document.getElementById('carrito');
    const btnCarrito = document.getElementById('btn-carrito');
    const overlay = document.getElementById('overlay');
    
    if (!carritoElement || !btnCarrito || !overlay) {
        console.error('Elementos del carrito no encontrados');
        return;
    }
    
    window.toggleCarrito = function() {
        const mostrar = !carritoElement.classList.contains('mostrar');
        carritoElement.classList.toggle('mostrar', mostrar);
        overlay.classList.toggle('mostrar', mostrar);
        document.body.style.overflow = mostrar ? 'hidden' : 'auto';
    };
    
    const nuevoBtnCarrito = btnCarrito.cloneNode(true);
    btnCarrito.parentNode.replaceChild(nuevoBtnCarrito, btnCarrito);
    
    const nuevoOverlay = overlay.cloneNode(true);
    overlay.parentNode.replaceChild(nuevoOverlay, overlay);
    
    document.getElementById('btn-carrito').addEventListener('click', function(e) {
        e.preventDefault();
        toggleCarrito();
    });
    
    document.getElementById('overlay').addEventListener('click', function() {
        toggleCarrito();
    });
}

document.addEventListener('DOMContentLoaded', function() {
    inicializarCarrito();
    
    document.getElementById('vaciar-carrito')?.addEventListener('click', vaciarCarrito);
    
    document.querySelectorAll('.formulario-agregar').forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const boton = this.querySelector('button[type="submit"]');
            const originalText = boton.innerHTML;
            
            try {
                boton.disabled = true;
                boton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Procesando...';
                
                const productoId = this.dataset.productoId;
                const productoNombre = this.dataset.productoNombre;
                const productoPrecio = parseFloat(this.dataset.productoPrecio);
                const cantidad = parseInt(this.querySelector('input[name="cantidad"]').value);
                const stock = parseInt(this.dataset.stock);
                
                if (cantidad < 1 || cantidad > stock) {
                    throw new Error(`Cantidad inválida. Máximo: ${stock}`);
                }
                
                await agregarAlCarrito({
                    producto_id: productoId,
                    cantidad: cantidad,
                    producto_nombre: productoNombre,
                    precio: productoPrecio * cantidad,
                    tipo_venta: 'unidad'
                });
                
                this.querySelector('input[name="cantidad"]').value = 1;
            } catch (error) {
                mostrarNotificacion(error.message, 'error');
            } finally {
                boton.disabled = false;
                boton.innerHTML = originalText;
            }
        });
    });
    
    document.querySelectorAll('.formulario-agregar-peso').forEach(form => {
        const pesoInput = form.querySelector('input[name="peso"]');
        if (pesoInput) {
            const stock = parseInt(form.dataset.stock);
            pesoInput.addEventListener('input', () => validarPeso(pesoInput, stock));
        }
        
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const boton = this.querySelector('button[type="submit"]');
            const originalText = boton.innerHTML;
            
            try {
                boton.disabled = true;
                boton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Procesando...';
                
                const productoId = this.dataset.productoId;
                const productoNombre = this.dataset.productoNombre;
                const productoPrecio = parseFloat(this.dataset.productoPrecio);
                const peso = parseInt(this.querySelector('input[name="peso"]').value);
                const stock = parseInt(this.dataset.stock);
                
                if (peso < 10 || peso > stock * 10) {
                    throw new Error(`Peso inválido. Rango: 10g - ${stock * 10}g`);
                }
                
                await agregarAlCarrito({
                    producto_id: productoId,
                    cantidad: 1,
                    unidades: peso / 10,
                    producto_nombre: `${productoNombre} (${peso}g)`,
                    precio: calcularPrecioPorPeso(peso, productoPrecio),
                    tipo_venta: 'peso'
                });
                
                this.querySelector('input[name="peso"]').value = 10;
                this.querySelector(`#unidades-${productoId}`).textContent = '1';
            } catch (error) {
                mostrarNotificacion(error.message, 'error');
            } finally {
                boton.disabled = false;
                boton.innerHTML = originalText;
            }
        });
    });
    
    const formPaquete = document.getElementById('form-paquete');
    if (formPaquete) {
        const selectProducto = formPaquete.querySelector('#producto-paquete');
        selectProducto.addEventListener('change', function() {
            const option = this.options[this.selectedIndex];
            if (option && option.value) {
                const precio = parseFloat(option.dataset.productoPrecio);
                document.getElementById('precio-1kg').textContent = (precio * 100).toFixed(2);
                document.getElementById('precio-700g').textContent = (precio * 70).toFixed(2);
                document.getElementById('precio-500g').textContent = (precio * 50).toFixed(2);
            }
        });
        
        formPaquete.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const boton = this.querySelector('button[type="submit"]');
            const originalText = boton.innerHTML;
            
            try {
                boton.disabled = true;
                boton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Procesando...';
                
                const select = this.querySelector('#producto-paquete');
                const productoId = select.value;
                const option = select.options[select.selectedIndex];
                
                if (!productoId) {
                    throw new Error('Seleccione un producto');
                }
                
                const productoNombre = option.dataset.productoNombre;
                const productoPrecio = parseFloat(option.dataset.productoPrecio);
                const stock = parseInt(option.dataset.stock);
                const tipoPaquete = this.querySelector('input[name="tipo-paquete"]:checked');
                const unidades = parseInt(tipoPaquete.dataset.unidades);
                const peso = tipoPaquete.value;
                
                if (unidades > stock) {
                    throw new Error(`Stock insuficiente. Disponible: ${stock} unidades`);
                }
                
                await agregarAlCarrito({
                    producto_id: productoId,
                    cantidad: 1,
                    unidades: unidades,
                    producto_nombre: `${productoNombre} (Paquete ${peso}g)`,
                    precio: productoPrecio * unidades,
                    tipo_venta: 'paquete'
                });
            } catch (error) {
                mostrarNotificacion(error.message, 'error');
            } finally {
                boton.disabled = false;
                boton.innerHTML = originalText;
            }
        });
    }
});

window.addEventListener('load', inicializarCarrito);