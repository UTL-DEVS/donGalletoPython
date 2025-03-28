var selected_device;
var devices = [];
// En HTML: Impresoras disponibles: <select id="selected_device" onchange=agregarImpresoraSeleccionada(this);></select>
function agregarImpresoraSeleccionada(selected) {
    for (var i = 0; i < devices.length; ++i) {
        if (selected.value == devices[i].uid) {
            selected_device = devices[i];
            return;
        }
    }
}
function buscarImpresoras() {
    //Get the default device from the application as a first step. Discovery takes longer to complete.
    BrowserPrint.getDefaultDevice("printer", function (device) {
        var html_select = document.getElementById("selected_device");
        //Discover any the devices available to the application
        BrowserPrint.getLocalDevices(function (device_list) {
            for (var i = 0; i < device_list.length; i++) {
                //Add device to list of devices and to html select element
                var device = device_list[i];
                if (!selected_device || device.uid != selected_device.uid) {
                    devices.push(device);
                    var option = document.createElement("option");
                    option.text = device.name;
                    option.value = device.uid;
                    html_select.add(option);
                }
            }
        }, function () {mostrarAlerta('error','Oops...','Error obteniendo los dispositivos locales','Asegurate de que la impresora esté conectada');
        }, "printer");

    }, function (error) {
        alert(error);
    })
}
 function mostrarAlerta(tipo,titulo,mensaje,pieVentana){
    Swal.fire({
        icon: tipo,
        title: titulo,
        text: mensaje,
        footer: '<p>'+pieVentana+'</p>'
      });
 }

function imprimirEnImpresoraSeleccionada(diseñoAImprimir) {
    selected_device.send(diseñoAImprimir, undefined, errorCallback);
}

var readCallback = function (readData) {
    if (readData === undefined || readData === null || readData === "") {
        mostrarAlerta('error','Oops...','La impresora no responde!','Asegurate de que la impresora tiene consumible, esté cerrada y conectada');
    }
    else {
        alert(readData);
    }
}
var errorCallback = function (errorMessage) {
    mostrarAlerta('error','Oops...',errorMessage,'');
}

function obtenerInfoImpresorasDetectadas(deviceList) {
    return (JSON.stringify(deviceList, null, 4))
}



window.onload = buscarImpresoras;
