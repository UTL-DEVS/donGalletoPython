function generarCorteVentas() {
    const btn = document.getElementById('corte-ventas');
    if (!btn) return;
    
    btn.addEventListener('click', async function() {
        try {
            const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
            if (!csrfToken) throw new Error("Token de seguridad no encontrado");
            
            btn.disabled = true;
            const originalText = btn.innerHTML;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Generando...';
            
            const response = await fetch('/api/corte_ventas', {
                headers: { 'X-CSRFToken': csrfToken }
            });
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || 'Error al generar el corte');
            }
            
            const data = await response.json();
            if (data.success && data.url) {
                window.open(data.url, '_blank');
            } else {
                throw new Error(data.error || 'Error en el servidor');
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarNotificacion(error.message, 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-file-alt"></i> Corte de Ventas';
        }
    });
}