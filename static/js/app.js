/* global bootstrap: false */
(() => {
    'use strict'
    const tooltipTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.forEach(tooltipTriggerEl => {
        new bootstrap.Tooltip(tooltipTriggerEl)
    })
})()

$(document).ready(function() {
    $('.sidebar a').on('click', function(e) {
        e.preventDefault();
        const url = $(this).attr('href');

        if (url != '/') {
            $.get(url, function(data) {
                $('.container-principal').html($(data).find('.container-principal').html());
                history.pushState(null, null, url);
            });
        } else {
            window.location.href = url; 
        }
    });
});

function actualizarTituloHistorial() {
    const fechaSeleccionada = document.getElementById('inpFecha').value;
    const tituloHistorial = document.getElementById('tituloHistorial');

    if (fechaSeleccionada) {
        const [anio, mes, dia] = fechaSeleccionada.split('-');
        const fechaFormateada = `${dia}/${mes}/${anio}`;
        tituloHistorial.textContent = `Historial - ${fechaFormateada}`;
    } else {
        tituloHistorial.textContent = 'Historial';
    }

    document.getElementById("formHistorial").submit()
}