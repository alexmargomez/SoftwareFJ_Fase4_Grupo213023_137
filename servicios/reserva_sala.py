from modelos.servicio import Servicio
from modelos.excepciones import DatosInvalidosError

class ReservaSala(Servicio):
    def __init__(self, nombre, costo_base, capacidad, horas_reserva, disponible=True):
        super().__init__(nombre, costo_base, disponible)
        self.capacidad = capacidad
        self.horas_reserva = horas_reserva

    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        costo = self.costo_base * self.horas_reserva
        costo += costo * impuesto
        costo -= costo * descuento
        return costo

    def describir_servicio(self):
        return f"Sala: {self.nombre} | Capacidad: {self.capacidad} pers. | Horas: {self.horas_reserva}"

    def validar_servicio(self):
        if self.capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser mayor a 0.")
        if self.horas_reserva <= 0:
            raise DatosInvalidosError("Las horas de reserva deben ser mayores a 0.")
        return True
