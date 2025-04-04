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

document.getElementById('btnProcesarProduccion').addEventListener('click', function () {
    const filas = document.querySelectorAll('#tblAgregarProduccion tbody tr');
    const datosGalletas = [];

    filas.forEach(fila => {
        const th = fila.querySelector('th[id]');
        const idGalleta = th ? th.id : null;

        const pCantidad = fila.querySelector('input[name="cantidad"]');
        const cantidad = pCantidad ? parseInt(pCantidad.value) : 0;

        if (idGalleta && !isNaN(cantidad)) {
            datosGalletas.push({
                id_galleta: idGalleta,
                cantidad: cantidad
            });
        }
    });

    enviarAlServicio(datosGalletas)
});

function enviarAlServicio(datos) {
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;
    
    fetch('/procesar-produccion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken 
        },
        body: JSON.stringify({ lstDetalleProduccion: datos })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success)
            alert(data.message)
            window.location = '/produccion-stock'
        if (data.error)
            alert(data.message)
    });
}