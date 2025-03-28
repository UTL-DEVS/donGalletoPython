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
