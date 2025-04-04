document.getElementById('btnSolicitar').addEventListener('click', function(event) {
    const filas = document.querySelectorAll('#tblSolicitudInsumos tbody tr');
    const solicitudes = [];

    filas.forEach(fila => {
        
        const th = fila.querySelector('th');
        const idMateria = th ? th.id : null;

        const pCantidad = fila.querySelector('input[name="cantidad"]');
        const cantidad = pCantidad ? parseInt(pCantidad.value) : 0;
        
        if (idMateria && !isNaN(cantidad)) {
            solicitudes.push({
                id_materia: idMateria,
                cantidad: cantidad
            });
        }
    });

    enviarAlServicio(solicitudes);
});

function enviarAlServicio(datos) {
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;
    console.log(datos)
    fetch('/solicitar-insumos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  
        },
        body: JSON.stringify({
            solicitudes: datos
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
