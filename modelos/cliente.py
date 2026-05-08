from modelos.entidad import Entidad
from modelos.excepciones import ClienteInvalidoError
import re

class Cliente(Entidad):
    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ClienteInvalidoError("El nombre no puede estar vacío.")
        self.__nombre = valor

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if not str(valor).isnumeric():
            raise ClienteInvalidoError("El documento debe ser numérico.")
        self.__documento = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(patron, valor):
            raise ClienteInvalidoError("El correo no tiene un formato válido.")
        self.__correo = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not str(valor).isnumeric() or len(str(valor)) < 7:
            raise ClienteInvalidoError("El teléfono debe ser numérico y tener al menos 7 dígitos.")
        self.__telefono = valor

    def mostrar_informacion(self):
        return f"Cliente: {self.nombre} | Doc: {self.documento} | Correo: {self.correo} | Tel: {self.telefono}"

    def __str__(self):
        return self.mostrar_informacion()
