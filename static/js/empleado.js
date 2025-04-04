function revisarModalesAbiertos() {
    d = new Boolean(modalesAbiertos.detalles);
    e = new Boolean(modalesAbiertos.editar);
    a = new Boolean(modalesAbiertos.agregar);
    console.log('Detalles: ' + d);
    console.log('Editar: ' + e);
    console.log('Add: ' + a);
    if (parseInt(modalesAbiertos.detalles)) {
        $('#modalDetallesEmpleado').modal('show');
        console.log('detalles');
    }
    if (parseInt(modalesAbiertos.editar)) {
        $('#modalEditarEmpleado').modal('show');
    }
    if (parseInt(modalesAbiertos.agregar)) {
        $('#modalAgregarEmpleado').modal('show');
    }
}

function ventanaConfirmarEliminacion(idProveedor){
    $('#confirmarEliminarEmpleado').modal('show');
    $('#btnEliminarEmpleado').attr('href','/empleado/eliminarEmpleado?id_prov_del='+idEmpleado);
}

function ventanaConfirmarReactivacion(idEmpleado){
    $('#confirmarReactivarEmpleado').modal('show');
    $('#btnReactivarEmpleado').attr('href','/proveedor/reactivarEmpleado?id_prov_rea='+idEmpleado);
}

$('#formularioEditarEmpleado').submit(function (event) {
    event.preventDefault();  // Evita el envío del formulario
    Swal.fire({
        title: "¿Estás segur@ de modificar este empleado?",
        text: "Se realizarán cambios en la base de datos",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Continuar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: "Hecho!",
                icon: "success"
            }).then(() => {
                event.target.submit(); // Envía el formulario
            });
        }
    });
});

window.onload = function () {
    revisarModalesAbiertos();
};
