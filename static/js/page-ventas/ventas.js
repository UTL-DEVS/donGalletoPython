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
                data-galleta-id="${item.galleta_id}"
                data-galleta-nombre="${item.nombre}"
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

            sessionStorage.setItem('carrito', JSON.stringify(data.carrito));
            actualizarVistaCarrito(data.carrito, data.nuevo_total);
            mostrarNotificacion(data.mensaje || 'Galleta agregada al carrito');
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
        const galletaId = this.dataset.galletaId;
        const galletaNombre = this.dataset.galletaNombre;
        const tipoVenta = this.dataset.tipoVenta;
        
        const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
        
        const response = await fetch(`/api/eliminar_del_carrito/${galletaId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                galleta_nombre: galletaNombre,
                tipo_venta: tipoVenta
            })
        });
        
        if (!response.ok) {
            throw new Error('Error al eliminar la galleta');
        }
        
        const data = await response.json();
        
        if (data.exito) {
            actualizarVistaCarrito(data.carrito, data.nuevo_total);
            mostrarNotificacion('Galleta eliminada del carrito');
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

            sessionStorage.removeItem('carrito');
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

async function procesarVenta() {
    const btnProcesar = document.getElementById('procesar-venta');
    if (btnProcesar) {
        btnProcesar.disabled = true;
        btnProcesar.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Procesando...';
    }

    try {
        const carrito = JSON.parse(sessionStorage.getItem('carrito') || '[]');
        
        if (!carrito.length) {
            mostrarNotificacion('El carrito está vacío', 'error');
            return;
        }

        const items = carrito.map(item => ({
            galleta_id: item.galleta_id,
            cantidad: item.cantidad || item.unidades || 1,
            precio_unitario: item.precio_unitario || (item.subtotal / (item.cantidad || item.unidades || 1)),
            subtotal: item.subtotal,
            tipo_venta: item.tipo_venta || 'unidad'
        }));

        const total = items.reduce((sum, item) => sum + item.subtotal, 0);
        const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

        const response = await fetch('/api/procesar_venta', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ items, total })
        });

        let data;
        try {
            data = await response.json(); // Intenta parsear la respuesta JSON
        } catch (e) {
            // Si falla el parseo JSON, muestra el texto de la respuesta
            const errorText = await response.text();
            throw new Error(`Respuesta inválida del servidor: ${errorText}`);
        }

        if (!response.ok) {
            // Muestra detalles del error del servidor
            const errorMsg = data.error || data.message || 'Error desconocido del servidor';
            console.error('Detalles del error:', {
                status: response.status,
                statusText: response.statusText,
                error: data.error,
                stack: data.stack // si está disponible
            });
            throw new Error(`Error ${response.status}: ${errorMsg}`);
        }

        // ... (resto del código para éxito)

    } catch (error) {
        console.error('Error completo:', error);
        mostrarNotificacion(error.message, 'error');
    } finally {
        if (btnProcesar) {
            btnProcesar.disabled = false;
            btnProcesar.innerHTML = 'Procesar Venta';
        }
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
    const galletaId = input.id.split('-')[1];
    const unidadesSpan = document.getElementById(`unidades-${galletaId}`);
    
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
    
    let carritoInicial = [];
    try {
        const carritoStr = sessionStorage.getItem('carrito');
        if (carritoStr) {
            carritoInicial = JSON.parse(carritoStr);
        }
    } catch (e) {
        console.error('Error parsing carrito from sessionStorage:', e);
        carritoInicial = [];
    }
    
    if (!Array.isArray(carritoInicial)) {
        carritoInicial = [];
    }
    
    const totalInicial = carritoInicial.reduce((sum, item) => sum + (item.subtotal || 0), 0);
    
    actualizarVistaCarrito(carritoInicial, totalInicial);

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

    document.getElementById('procesar-venta')?.addEventListener('click', procesarVenta);
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
                
                const galletaId = this.dataset.galletaId;
                const galletaNombre = this.dataset.galletaNombre;
                const galletaPrecio = parseFloat(this.dataset.galletaPrecio);
                const cantidad = parseInt(this.querySelector('input[name="cantidad"]').value);
                const stock = parseInt(this.dataset.stock);
                
                if (cantidad < 1 || cantidad > stock) {
                    throw new Error(`Cantidad inválida. Máximo: ${stock}`);
                }
                
                await agregarAlCarrito({
                    galleta_id: galletaId,
                    cantidad: cantidad,
                    galleta_nombre: galletaNombre,
                    precio: galletaPrecio * cantidad,
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
                
                const galletaId = this.dataset.galletaId;
                const galletaNombre = this.dataset.galletaNombre;
                const galletaPrecio = parseFloat(this.dataset.galletaPrecio);
                const peso = parseInt(this.querySelector('input[name="peso"]').value);
                const stock = parseInt(this.dataset.stock);
                
                if (peso < 10 || peso > stock * 10) {
                    throw new Error(`Peso inválido. Rango: 10g - ${stock * 10}g`);
                }
                
                await agregarAlCarrito({
                    galleta_id: galletaId,
                    cantidad: 1,
                    unidades: peso / 10,
                    galleta_nombre: `${galletaNombre} (${peso}g)`,
                    precio: calcularPrecioPorPeso(peso, galletaPrecio),
                    tipo_venta: 'peso'
                });
                
                this.querySelector('input[name="peso"]').value = 10;
                this.querySelector(`#unidades-${galletaId}`).textContent = '1';
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
        const selectGalleta = formPaquete.querySelector('#galleta-paquete');
        selectGalleta.addEventListener('change', function() {
            const option = this.options[this.selectedIndex];
            if (option && option.value) {
                const precio = parseFloat(option.dataset.galletaPrecio);
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
                
                const select = this.querySelector('#galleta-paquete');
                const galletaId = select.value;
                const option = select.options[select.selectedIndex];
                
                if (!galletaId) {
                    throw new Error('Seleccione una galleta');
                }
                
                const galletaNombre = option.dataset.galletaNombre;
                const galletaPrecio = parseFloat(option.dataset.galletaPrecio);
                const stock = parseInt(option.dataset.stock);
                const tipoPaquete = this.querySelector('input[name="tipo-paquete"]:checked');
                const unidades = parseInt(tipoPaquete.dataset.unidades);
                const peso = tipoPaquete.value;
                
                if (unidades > stock) {
                    throw new Error(`Stock insuficiente. Disponible: ${stock} unidades`);
                }
                
                await agregarAlCarrito({
                    galleta_id: galletaId,
                    cantidad: 1,
                    unidades: unidades,
                    galleta_nombre: `${galletaNombre} (Paquete ${peso}g)`,
                    precio: galletaPrecio * unidades,
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