function revisarModalAbierto() {
    console.log('open? '+modalOpen)
    if ((modalOpen)) {
        $('#modalDetallesEmpleado').modal('show');
    }
}

window.onload = function () {
    revisarModalAbierto();
};
