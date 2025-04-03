import datetime

class ResumenVentaCQRS:
    @staticmethod
    def validar_fecha_corte(fecha):
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            return True, "Fecha válida"
        except ValueError:
            return False, "Formato de fecha no válido, debe ser YYYY-MM-DD"