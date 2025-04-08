function ventanaConfirmarPago(idEmp){
    $('#confirmarPagarEmpleado').modal('show');
    $('#btnPagarEmpleado').attr('href','/economia/nomina/pago?id_emp='+idEmp);
}

function consultarNomina() {
    const fechaSeleccionada = document.getElementById('inpFecha').value;
    const quincenaSel = document.getElementById('quin').value;

    if (fechaSeleccionada) {
        //document.getElementById("formConsultarNomina").submit()
        window.location.assign('/economia/nomina?fechaSel=' + fechaSeleccionada + '&quincena=' + quincenaSel);
    }
}