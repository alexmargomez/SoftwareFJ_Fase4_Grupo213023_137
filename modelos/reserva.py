from modelos.excepciones import ReservaError, ServicioNoDisponibleError
from utils.logger import logger

class Reserva:
    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def validar_datos(self):
        if not self.cliente:
            raise ReservaError("Cliente no válido.")
        if not self.servicio:
            raise ReservaError("Servicio no válido.")
        if self.duracion <= 0:
            raise ReservaError("La duración debe ser mayor a 0.")
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.servicio.nombre}' no está disponible.")
        self.servicio.validar_servicio()

    def confirmar(self):
        if self.estado == "Pendiente":
            self.estado = "Confirmada"
            logger.info(f"Reserva confirmada para {self.cliente.nombre} - Servicio: {self.servicio.nombre}")
        else:
            raise ReservaError(f"No se puede confirmar una reserva en estado: {self.estado}")

    def cancelar(self):
        if self.estado != "Cancelada":
            self.estado = "Cancelada"
            logger.info(f"Reserva cancelada para {self.cliente.nombre} - Servicio: {self.servicio.nombre}")
        else:
            raise ReservaError("La reserva ya está cancelada.")

    def procesar_reserva(self):
        try:
            logger.info(f"Iniciando procesamiento de reserva para {self.cliente.nombre if self.cliente else 'Cliente desconocido'}")
            self.validar_datos()
            self.confirmar()
            print(f"Reserva procesada con éxito: {self.servicio.describir_servicio()} por un costo de ${self.servicio.calcular_costo():.2f}")
        except (ReservaError, ServicioNoDisponibleError) as e:
            logger.error(f"Error al procesar reserva: {e}")
            raise e
        except Exception as e:
            logger.critical(f"Error inesperado al procesar reserva: {e}")
            raise ReservaError("Error interno al procesar la reserva.") from e
        finally:
            logger.debug(f"Fin del intento de procesamiento de reserva para {self.cliente.nombre if self.cliente else 'desconocido'}")
