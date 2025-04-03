
// Navbar scroll effect mejorado
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    const logo = document.querySelector('.logo');
    
    if (window.scrollY > 100) {
        navbar.classList.add('scrolled');
        logo.style.height = '40px';
    } else {
        navbar.classList.remove('scrolled');
        logo.style.height = '50px';
    }
});

// Smooth scrolling mejorado para navegación
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
            
            // Cerrar menú en móviles después de hacer clic
            const navbarCollapse = document.querySelector('.navbar-collapse');
            if (navbarCollapse.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                    toggle: false
                });
                bsCollapse.hide();
            }
        }
    });
});

// Animación al hacer scroll mejorada
function animateOnScroll() {
    const elements = document.querySelectorAll('.animate__animated');
    const windowHeight = window.innerHeight;
    const triggerPoint = windowHeight / 1.2;
    
    elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        
        if (elementPosition < triggerPoint) {
            const animationClass = element.classList[1];
            element.classList.add(animationClass);
        }
    });
}

// Ejecutar al cargar y al hacer scroll
window.addEventListener('load', animateOnScroll);
window.addEventListener('scroll', animateOnScroll);

// Validación de formulario mejorada
(function() {
    'use strict';
    
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
})();

// Mostrar más galletas al hacer clic en el botón
document.getElementById('ver-mas-btn').addEventListener('click', function() {
const masGalletas = document.getElementById('mas-galletas');
const boton = this;

if (masGalletas.classList.contains('d-none')) {
  masGalletas.classList.remove('d-none');
  masGalletas.classList.add('animate__animated', 'animate__fadeIn');
  boton.textContent = 'Mostrar Menos';
} else {
  masGalletas.classList.add('d-none');
  boton.textContent = 'Ver Más Sabores';
}
});
         // Mostrar/ocultar galletas adicionales
  document.addEventListener("DOMContentLoaded", function () {
const verMasBtn = document.getElementById("ver-mas-btn");
const masGalletas = document.getElementById("mas-galletas");

if (verMasBtn && masGalletas) {
verMasBtn.addEventListener("click", function () {
    masGalletas.classList.remove("d-none");
    verMasBtn.style.display = "none"; 
});
}
});
