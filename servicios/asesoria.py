from modelos.servicio import Servicio
from modelos.excepciones import DatosInvalidosError

class AsesoriaEspecializada(Servicio):
    def __init__(self, nombre, costo_base, especialista, horas_asesoria, disponible=True):
        super().__init__(nombre, costo_base, disponible)
        self.especialista = especialista
        self.horas_asesoria = horas_asesoria

    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        costo = self.costo_base * self.horas_asesoria
        costo += costo * impuesto
        costo -= costo * descuento
        return costo

    def describir_servicio(self):
        return f"Asesoría: {self.nombre} | Especialista: {self.especialista} | Horas: {self.horas_asesoria}"

    def validar_servicio(self):
        if not self.especialista:
            raise DatosInvalidosError("El especialista no puede estar vacío.")
        if self.horas_asesoria <= 0:
            raise DatosInvalidosError("Las horas de asesoría deben ser mayores a 0.")
        return True
