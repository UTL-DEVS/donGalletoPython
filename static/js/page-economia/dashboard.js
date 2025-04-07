document.getElementById("mesGraficaVentasDiarias").addEventListener("input", function () {
  let mesSeleccionado = new Date(Date.parse(this.value)); // Formato: YYYY-MM
  let primerMesVenta = "01/2025";
  let ultimoMesVenta = "04/2025";
  if (rangosFechasVentas != undefined) {
    let [primerMes, primerAnio] = rangosFechasVentas.primera_venta.split('/');
    let [ultimoMes, ultimoAnio] = rangosFechasVentas.ultima_venta.split('/');

    primerMesVenta = new Date(parseInt(primerAnio), parseInt(primerMes) - 1, 1); // Año, Mes (0-based), Día
    ultimoMesVenta = new Date(parseInt(ultimoAnio), parseInt(ultimoMes) - 1, 1);

  }

  console.log('Mes sel: ' + mesSeleccionado);
  console.log('Primer mes: ' + primerMesVenta);
  console.log('Ultimo mes: ' + ultimoMesVenta);
  if (mesSeleccionado < primerMesVenta || mesSeleccionado > ultimoMesVenta) {
    $('#alertaMesFueraDeRango').modal('show');
    this.value = ""; // Borra la selección
  } else {
    let mesVentas = ('0' + (mesSeleccionado.getMonth() + 1)).slice(-2) + '/' + mesSeleccionado.getFullYear();
    window.location.assign('/economia/?mes_ventas=' + mesVentas + '&dias_ventas=' + 28);
  }
});
function cambiarFechaGrafica() {

}

function cargarGrafica(fechasVentas, totalesVentas) {
  console.log('Ventas¿ 1: '+totalesVentas[0]);

  var options = {
    series: [{
      name: 'Ventas',
      data: totalesVentas  // Usamos los totales de las ventas
    }],
    chart: {
      height: 350,
      type: 'bar',
      events: {
        click: function (chart, w, e) {
          console.log(chart, w, e)
        }
      }
    },
    plotOptions: {
      bar: {
        columnWidth: '45%',
        distributed: true,
      }
    },
    dataLabels: {
      enabled: false
    },
    legend: {
      show: false
    },
    xaxis: {
      categories: fechasVentas,
      labels: {
        style: {
          fontSize: '12px'
        }
      }
    }
  };

  var chart = new ApexCharts(document.querySelector("#ventasDiarias"), options);
  chart.render();
}

function obtenerDatosParaGrafica() {
  if(typeof listasVentasDiarias == "undefined" ){
    $('#ventasDiarias').text('No hay ventas para mostrar');
    return;
  }
  // Extraer los días y totales de las ventas
  let fechasVentas = listasVentasDiarias.map(venta => {
    let fecha = new Date(venta.fecha_venta);  // Convierte la fecha en objeto Date
    return fecha.getDate();  // Devuelve solo el día del mes
  });
  let totalesVentas = listasVentasDiarias.map(venta => venta.total);  // Extrae los totales
  console.log('totalv: ' + listasVentasDiarias[0].total)
  console.log('fechas_' + fechasVentas);
  console.log('totasles: ' + totalesVentas);
  cargarGrafica(fechasVentas, totalesVentas);

  const meses = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
];

    let fecha = new Date(listasVentasDiarias[0].fecha_venta);  // Convierte la fecha en objeto Date
    let mes = fecha.getMonth();  // El mes es 0-indexado, no hace falta sumarle 1
    let anio = fecha.getFullYear();
  $('#fechaGrafica').text(`${meses[mes]} ${anio}`);

}

window.onload = function () {
  obtenerDatosParaGrafica();
};