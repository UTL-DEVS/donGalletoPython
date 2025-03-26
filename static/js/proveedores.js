function detallesProveedor(posicionProvSel, callback) {
    url = "/detallesProveedor?posicionProvSel=" + posicionProvSel;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            callback(data);
        })
    .catch(error=>{
        console.error("Error al obtener datos:", error)
        callback(null)
    })
}

function mostrarDetallesProveedorModificar(posicionProvSel) {
    console.log('Posicion en modificar');
    detallesProveedor(posicionProvSel, function(proveedorSel){
        if (proveedorSel != null && proveedorSel != '') {
            $("#editNombreProveedorSel").html(proveedorSel.nombre);
            $("#editNombreRepresentanteProveedorSel").val(proveedorSel.representante);
            $("#editCorreoProveedorSel").val(proveedorSel.correo);
            $("#editTelefonoProveedorSel").val(proveedorSel.telefono);
            $("#editDireccionProveedorSel").val(proveedorSel.direccion);
        } else {
            alert('Error al obtener los detalles de proveedor')
        }
       
    });
}

function mostrarConsultaDetallesProveedor(posicionProvSel) {
    console.log('Posicion en consultar');
    detallesProveedor(posicionProvSel, function (proveedorSel) {
        if (proveedorSel != null && proveedorSel != '') {
            $("#nombreProveedorSel").html(proveedorSel.nombre);
            $("#nombreRepresentanteProveedorSel").html(proveedorSel.representante);
            $("#correoProveedorSel").html(proveedorSel.correo);
            $("#telefonoProveedorSel").html(proveedorSel.telefono);
            $("#direccionProveedorSel").html(proveedorSel.direccion);
        } else {
            alert('Error al obtener los detalles de proveedor')
        }
    });
}

