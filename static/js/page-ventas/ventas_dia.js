document.addEventListener("DOMContentLoaded", function () {
    $("#tablaVentas").DataTable({
      language: {
        url: "https://cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json",
      },
      order: [[2, "desc"]],
      responsive: true,
      dom: '<"top"lf>rt<"bottom"ip>',
      pageLength: 10,
      scrollY: "400px",
      scrollCollapse: true,
      paging: true,
      fixedHeader: true,
      initComplete: function () {
        this.api().columns.adjust();
      },
    });

    $(".ver-ticket").click(function () {
      const ventaId = $(this).data("venta-id");
      const ticketUrl = `/tickets/${ventaId}?view=1`;

      $("#modalVentaId").text(ventaId);
      $("#ticketIframe").attr("src", ticketUrl);
      $("#downloadTicketBtn").attr("href", `/tickets/${ventaId}`);
      $("#ticketModal").modal("show");
    });
  });