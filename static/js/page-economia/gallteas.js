document.getElementById("mesGraficaVentasGalletas").addEventListener("input", function () {
    let value = this.value; // "2025-04"
    let [anio, mes] = value.split("-");
  
    let mesSeleccionado = new Date(parseInt(anio), parseInt(mes) - 1); // Correcto, sin problemas de zona horaria
  
    let primerMesVenta = new Date(2025, 0); // Enero 2025
    let ultimoMesVenta = new Date(2025, 3); // Abril 2025
  
    if (rangosFechasVentas !== undefined) {
      let [primerMes, primerAnio] = rangosFechasVentas.primera_venta.split('/');
      let [ultimoMes, ultimoAnio] = rangosFechasVentas.ultima_venta.split('/');
      primerMesVenta = new Date(parseInt(primerAnio), parseInt(primerMes) - 1);
      ultimoMesVenta = new Date(parseInt(ultimoAnio), parseInt(ultimoMes) - 1);
    }
  
    if (mesSeleccionado < primerMesVenta || mesSeleccionado > ultimoMesVenta) {
      $('#alertaMesFueraDeRango').modal('show');
      this.value = ""; // Borra la selección
    } else {
      let mesVentas = mes + '/' + anio;
      window.location.assign('/economia/galletas?mes_ventas=' + mesVentas + '&dias_ventas=28');
    }
  });
  
  
  
  function cargarGrafica() {
  
    var options = {
        series: listasVentasGalletas,
        chart: {
        height: 350,
        type: 'line',
        zoom: {
          enabled: false
        },
        animations: {
          enabled: false
        }
      },
      stroke: {
        width: [5,5,4],
        curve: 'smooth'
      },
      labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
      title: {
        text: ''
      },
      xaxis: {
      },
      };

      var chart = new ApexCharts(document.querySelector("#galletasMasVendidas"), options);
      chart.render();
    
  }
  
  function obtenerDatosParaGrafica() {
    if(typeof listasVentasGalletas == "undefined" ){
        $('#galletasMasVendidas').text('No hay datos para mostrar');
        return;
      }
    cargarGrafica();
  
    const meses = [
      'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
  ];
  console.log(mes_sel);
  
    let partes = mes_sel.split('/');  // ["04", "2025"]
    let mes = parseInt(partes[0]) - 1;  // Restamos 1 porque enero = 0
    let anio = parseInt(partes[1]);
    $('#fechaGrafica').text(`${meses[mes]} ${anio}`);
  
  }
  
  window.onload = function () {
   
    obtenerDatosParaGrafica();
  };