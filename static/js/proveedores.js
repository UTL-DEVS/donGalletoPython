
//const modalesAbiertos = {{ modales|safe }};
function revisarModalesAbiertos() {
    d = new Boolean(modalesAbiertos.detalles);
    e = new Boolean(modalesAbiertos.editar);
    a = new Boolean(modalesAbiertos.agregar);
    console.log('Detalles: ' + d);
    console.log('Editar: ' + e);
    console.log('Add: ' + a);
    if (parseInt(modalesAbiertos.detalles)) {
        $('#modalDetallesProveedor').modal('show');
        console.log('detalles');
    }
    if (parseInt(modalesAbiertos.editar)) {
        $('#modalEditarProveedor').modal('show');
    }
    if (parseInt(modalesAbiertos.agregar)) {
        $('#modalAgregarProveedor').modal('show');
    }
}

function ventanaConfirmarEliminacion(idProveedor){
    $('#confirmarEliminarProveedor').modal('show');
    $('#btnEliminarProveedor').attr('href','/proveedor/eliminarProveedor?id_prov_del='+idProveedor);
}

function ventanaConfirmarReactivacion(idProveedor){
    $('#confirmarReactivarProveedor').modal('show');
    $('#btnReactivarProveedor').attr('href','/proveedor/reactivarProveedor?id_prov_rea='+idProveedor);
}

$('#formularioEditarProveedor').submit(function (event) {
    event.preventDefault();  // Evita el envío del formulario
    Swal.fire({
        title: "¿Estás segur@ de modificar este proveedor?",
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


function mostrarAlerta(tipo, titulo, mensaje, pieVentana) {
    Swal.fire({
        icon: tipo,
        title: titulo,
        text: mensaje,
        footer: '<p>' + pieVentana + '</p>'
    });
}

window.onload = function () {
    revisarModalesAbiertos();
};
