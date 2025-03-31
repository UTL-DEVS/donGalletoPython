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

function generarCorteVentas() {
    const btn = document.getElementById('corte-ventas');
    if (!btn) return;
    
    btn.addEventListener('click', async function() {
        try {
            const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
            if (!csrfToken) {
                alert("Token de seguridad no encontrado");
                return;
            }
            
            btn.disabled = true;
            const originalText = btn.innerHTML;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Generando...';
            
            const response = await fetch('/api/corte_ventas', {
                headers: { 
                    'X-CSRFToken': csrfToken,
                    'Accept': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Error al generar el corte');
            }
            
            if (data.success && data.url) {
                // Abrir en nueva pestaña
                window.open(data.url, '_blank');
            } else {
                throw new Error(data.error || 'Error en el servidor');
            }
        } catch (error) {
            console.error('Error:', error);
            alert(error.message); // Reemplazo temporal para mostrarNotificacion
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-file-alt"></i> Corte de Ventas';
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    generarCorteVentas();
});