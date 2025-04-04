function ventanaConfirmarPago(idEmp){
    $('#confirmarPagarEmpleado').modal('show');
    $('#btnPagarEmpleado').attr('href','/economia/nomina/pago?id_emp='+idEmp);
}
