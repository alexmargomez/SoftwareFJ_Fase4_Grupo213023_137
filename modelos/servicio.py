from abc import ABC, abstractmethod

class Servicio(ABC):
    def __init__(self, nombre, costo_base, disponible=True):
        self.nombre = nombre
        self.costo_base = costo_base
        self.disponible = disponible

    @abstractmethod
    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_servicio(self):
        pass
