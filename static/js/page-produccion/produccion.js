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
    const filas = document.querySelectorAll('#tablaDinamica tbody tr');

    const datos = Array.from(filas).map(fila => {
        const celdas = fila.querySelectorAll('td');

        return {
            campo1: celdas[0].querySelector('input').value,
            campo2: celdas[1].querySelector('input').value
        };
    });

    console.log(datos);

    enviarAlServicio(datos);
});

function enviarAlServicio(datos) {
    fetch('url-de-tu-servicio', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ items: datos })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Éxito:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}