function updateQuantity(button, isIncrement) {
    const container = button.closest('.opcion');
    const quantityElement = container.querySelector('.quantity');
    const cookiesElement = container.querySelector('.cookies-count');
    
    let currentQuantity = parseInt(quantityElement.textContent);
    let currentCookies = parseInt(cookiesElement.textContent);
    let newQuantity = currentQuantity;
    let newCookies = currentCookies;
    
    if (isIncrement) {
        newQuantity = currentQuantity + 1;
        newCookies = currentCookies + 10;
    } else {
        newQuantity = Math.max(0, currentQuantity - 1);
        newCookies = Math.max(0, currentCookies - 10);
        
        if (newQuantity === 0) {
            newCookies = 0;
        }
    }
    
    quantityElement.textContent = newQuantity;
    cookiesElement.textContent = newCookies + ' Galletas';
}

document.getElementById('enviarDatos').addEventListener('click', function () {
    const filas = document.querySelectorAll('#tblAgregarProduccion tbody tr');
    const datosGalletas = [];

    filas.forEach(fila => {
        const th = fila.querySelector('th[id]');
        const idGalleta = th ? th.id : null;

        const pCantidad = fila.querySelector('b[name="cantidad"]');
        const cantidad = pCantidad ? parseInt(pCantidad.textContent) : 0;

        if (idGalleta && !isNaN(cantidad)) {
            datosGalletas.push({
                id_galleta: idGalleta,
                cantidad: cantidad
            });
        }
    });

    console.log(datosGalletas)
    enviarAlServicio(datosGalletas)
});

function enviarAlServicio(datos) {
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    fetch('/agregarProduccion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  // ¡Agrega el token aquí!
        },
        body: JSON.stringify({ lstDetalleProduccion: datos })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.success)
            alert(data.message)
            window.location = '/produccion-stock'
        if (data.error)
            alert(data.message)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}