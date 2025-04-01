
let carrito = document.getElementById('carrito');
let btnCarrito = document.getElementById('btn-carrito');
let overlay = document.getElementById('overlay');

btnCarrito.addEventListener('click', () => {
    carrito.classList.toggle('mostrar');
    overlay.classList.toggle('mostrar');
});

overlay.addEventListener('click', () => {
    carrito.classList.remove('mostrar');
    overlay.classList.remove('mostrar');
});

// Actualizar precio total cuando cambia la cantidad
document.querySelectorAll('input[name="cantidad"]').forEach(input => {
input.addEventListener('change', function() {
    const form = this.closest('form');
    const priceText = form.querySelector('button').textContent;
    const priceMatch = priceText.match(/\$([\d.]+)/);
    
    if (priceMatch) {
        const price = parseFloat(priceMatch[1]);
        const newQuantity = parseInt(this.value) || 1;
        const unitPrice = galletas.find(g => g.id_galleta == form.id_galleta.value).precio_galleta;
        form.querySelector('button').textContent = 
            `Agregar al carrito - $${(unitPrice * newQuantity).toFixed(2)}`;
    }
});
});

// Manejar el carrito desplegable
document.getElementById('btn-carrito').addEventListener('click', function() {
const carrito = document.getElementById('carrito');
const overlay = document.getElementById('overlay');

if (carrito.style.display === 'block') {
    carrito.style.display = 'none';
    overlay.style.display = 'none';
} else {
    carrito.style.display = 'block';
    overlay.style.display = 'block';
}
});

// Cerrar carrito al hacer clic en el overlay
document.getElementById('overlay').addEventListener('click', function() {
document.getElementById('carrito').style.display = 'none';
this.style.display = 'none';
});