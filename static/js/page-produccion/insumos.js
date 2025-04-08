document.getElementById('btnSolicitar').addEventListener('click', function(event) {
    const filas = document.querySelectorAll('#tblSolicitudInsumos tbody tr');
    const solicitudes = [];
    let totalCompra = 0;
    filas.forEach(fila => {
        
        const th = fila.querySelector('th');
        const idMateria = th ? th.id : null;

        const inpPrecio = fila.querySelector('input[name="precio"]');
        const precio = inpPrecio ? parseInt(inpPrecio.value) : 0;
        const inpCantidad = fila.querySelector('input[name="cantidad"]');
        const cantidad = inpCantidad ? parseInt(inpCantidad.value) : 0;
        const inpCompra = fila.querySelector('input[name="compra"]');
        const compra = inpCompra ? parseInt(inpCompra.value) : 0;
        const inpTipo = fila.querySelector('input[name="tipo"]');
        const tipo = inpTipo ? parseInt(inpTipo.value) : 0;

        if (cantidad == 0) {
            return;
        }

        totalCompra += precio * cantidad
        
        if (idMateria && !isNaN(cantidad)) {
            solicitudes.push({
                id_materia: idMateria,
                cantidad: cantidad,
                compra: compra,
                tipo: tipo,
                precio: precio
            });
        }
    });

    enviarAlServicio(solicitudes, totalCompra);
});

function enviarAlServicio(datos, total) {
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;
    console.log(datos)
    fetch('/solicitar-insumos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  
        },
        body: JSON.stringify({
            solicitudes: datos,
            totalCompra: total
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.success)
            alert(data.message)
            window.location = '/cocina-insumos'
        if (data.error)
            alert(data.message)
    })
}

function updateQuantity(button, isIncrement) {
    const container = button.closest('.opcion');
    const quantityElement = container.querySelector('.quantity');
    
    let currentQuantity = parseInt(quantityElement.value);
    let newQuantity = currentQuantity;
    
    if (isIncrement) {
        newQuantity = currentQuantity + 1;
    } else {
        newQuantity = Math.max(0, currentQuantity - 1);
        
        if (newQuantity === 0) {
            newCookies = 0;
        }
    }
    
    quantityElement.value = newQuantity;
}
