from modelos.servicio import Servicio
from modelos.excepciones import DatosInvalidosError

class AlquilerEquipo(Servicio):
    def __init__(self, nombre, costo_base, tipo_equipo, dias_alquiler, disponible=True):
        super().__init__(nombre, costo_base, disponible)
        self.tipo_equipo = tipo_equipo
        self.dias_alquiler = dias_alquiler

    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        costo = self.costo_base * self.dias_alquiler
        costo += costo * impuesto
        costo -= costo * descuento
        return costo

    def describir_servicio(self):
        return f"Equipo: {self.nombre} ({self.tipo_equipo}) | Días: {self.dias_alquiler}"

    def validar_servicio(self):
        if not self.tipo_equipo:
            raise DatosInvalidosError("El tipo de equipo no puede estar vacío.")
        if self.dias_alquiler <= 0:
            raise DatosInvalidosError("Los días de alquiler deben ser mayores a 0.")
        return True
