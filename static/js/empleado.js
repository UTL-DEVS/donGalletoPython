function revisarModalesAbiertos() {
    if (parseInt(modalesAbiertos.detalles)) {
        $('#modalDetallesEmpleado').modal('show');
    }
    if (parseInt(modalesAbiertos.editar)) {
        $('#modalEditarEmpleado').modal('show');
    }
    if (parseInt(modalesAbiertos.agregar)) {
        $('#modalAgregarEmpleado').modal('show');
    }
}

function ventanaConfirmarEliminacion(idEmpleado){
    $('#confirmarEliminarEmpleado').modal('show');
    $('#btnEliminarEmpleado').attr('href','/navegante/empleado/eliminarEmpleado?id_emp_del='+idEmpleado);
}

function ventanaConfirmarReactivacion(idEmpleado){
    $('#confirmarReactivarProveedor').modal('show');
    $('#btnReactivarEmpleado').attr('href','/navegante/empleado/reactivarEmpleado?id_emp_rea='+idEmpleado);
}


/*function ventanaConfirmarReactivacion(idEmpleado){
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
});*/
 function ventanaConfirmarEdicion(){
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
                $("#formularioEditarEmpleado").submit();
            });
        }
    });
 }

window.onload = function () {
    revisarModalesAbiertos();
};
