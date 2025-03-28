function detallesProveedor(idProv, callback) {
    url = "/proveedor/detallesProveedor?id_prov=" + idProv;
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
    detallesProveedor(posicionProvSel, function(proveedorSel){
        if (proveedorSel != null && proveedorSel != '') {
            $("#modificarProveedor  #nombreProveedor").html(proveedorSel.nombre);
            $("#modificarProveedor  .nombrePersona").val(proveedorSel.nombreRepresentante);
            $("#modificarProveedor  .primerApellidoPersona").val(proveedorSel.primerApellidoRepresentante);
            $("#modificarProveedor  .segundoApellidoPersona").val(proveedorSel.segundoApellidoRepresentante);
            $("#modificarProveedor  .direccionPersona").val(proveedorSel.direccion);
            $("#modificarProveedor  .correoPersona").val(proveedorSel.correo);
            $("#modificarProveedor  .telefonoPersona").val(proveedorSel.telefono);
            $("#modificarProveedor").attr('action','/proveedor/actualizarProveedor?id_prov_upd='+proveedorSel.id_proveedor);

        } else {
            alert('Error al obtener los detalles de proveedor')
        }
       
    });
}

function mostrarConsultaDetallesProveedor(idProv) {
    detallesProveedor(idProv, function (proveedorSel) {
        if (proveedorSel != null && proveedorSel != '') {
            $("#nombreProveedorSel").html(proveedorSel.nombre);
            $("#nombreRepresentanteProveedorSel").html(proveedorSel.nombreRepresentante+' '+proveedorSel.primerApellidoRepresentante+' '+proveedorSel.segundoApellidoRepresentante );
            $("#correoProveedorSel").html(proveedorSel.correo);
            $("#telefonoProveedorSel").html(proveedorSel.telefono);
            $("#direccionProveedorSel").html(proveedorSel.direccion);
        } else {
            alert('Error al obtener los detalles de proveedor')
        }
    });
}

function confirmarModificacionProveedor(){
    Swal.fire({
        title: "¿Estás segur@ de modificar este proveedor?",
        text: "Se realizarán cambios en la base de datos",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Continuar",
        cancelButtonText: ""
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire({
            title: "Hecho!",
            icon: "success"
          });
          return true;
        }
      });
      return false;
}

function mostrarAlerta(tipo,titulo,mensaje,pieVentana){
    Swal.fire({
        icon: tipo,
        title: titulo,
        text: mensaje,
        footer: '<p>'+pieVentana+'</p>'
      });
 }

