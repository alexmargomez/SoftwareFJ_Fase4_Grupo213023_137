from abc import ABC, abstractmethod
from datetime import datetime
import uuid

class Entidad(ABC):
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.fecha_creacion = datetime.now()

    @abstractmethod
    def mostrar_informacion(self):
        pass
