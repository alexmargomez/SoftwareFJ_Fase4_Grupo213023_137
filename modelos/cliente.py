from modelos.entidad import Entidad
from modelos.excepciones import ClienteInvalidoError
import re

class Cliente(Entidad):
    """
    Clase que representa a un cliente del sistema Software FJ.
    
    MEJORA: Se agregaron validaciones más rigurosas para garantizar la integridad
    de los datos personales del cliente. Esto incluye:
    - Validación de longitud mínima de nombre (3 caracteres)
    - Validación de longitud mínima de documento (5 dígitos)
    - Validación de longitud máxima de teléfono (15 dígitos para estándares internacionales)
    - Encadenamiento de excepciones para mejor trazabilidad de errores
    
    PRINCIPIO APLICADO: Encapsulación y validación robusta de datos.
    """
    
    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()
        # Se inicializan los atributos usando los setters para aplicar validaciones
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        # MEJORA: Se agrega una lista para rastrear el historial de reservas del cliente
        self.__historial_reservas = []

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        """
        MEJORA: Validación mejorada de nombre.
        - Verifica que no esté vacío
        - Verifica que tenga al menos 3 caracteres (después del strip)
        - Usa encadenamiento de excepciones para mejor contexto de error
        """
        try:
            if not valor or not valor.strip():
                raise ValueError("El nombre no puede estar vacío.")
            if len(valor.strip()) < 3:
                raise ValueError("El nombre debe tener al menos 3 caracteres.")
        except ValueError as e:
            # MEJORA: Encadenamiento de excepciones - proporciona contexto de qué validación falló
            raise ClienteInvalidoError(f"Validación de nombre fallida: {e}") from e
        
        self.__nombre = valor.strip()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        """
        MEJORA: Validación mejorada de documento.
        - Verifica que sea numérico
        - Verifica que tenga al menos 5 dígitos (evita números muy cortos)
        - Usa encadenamiento de excepciones
        """
        try:
            valor_str = str(valor).strip()
            if not valor_str.isnumeric():
                raise ValueError("El documento debe ser numérico.")
            if len(valor_str) < 5:
                raise ValueError("El documento debe tener al menos 5 dígitos.")
        except ValueError as e:
            # MEJORA: Encadenamiento de excepciones
            raise ClienteInvalidoError(f"Validación de documento fallida: {e}") from e
        
        self.__documento = valor_str

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        """
        Validación de formato de correo usando expresión regular.
        MANTIENE: La validación original de email que ya funcionaba bien.
        """
        try:
            patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(patron, valor):
                raise ValueError("Formato de correo inválido.")
        except ValueError as e:
            raise ClienteInvalidoError(f"Validación de correo fallida: {e}") from e
        
        self.__correo = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        """
        MEJORA: Validación mejorada de teléfono.
        - Verifica que sea numérico
        - Verifica que tenga al menos 7 dígitos (mínimo internacional)
        - Verifica que no exceda 15 dígitos (máximo estándar E.164)
        - Usa encadenamiento de excepciones
        """
        try:
            valor_str = str(valor).strip()
            if not valor_str.isnumeric():
                raise ValueError("El teléfono debe ser numérico.")
            if len(valor_str) < 7:
                raise ValueError("El teléfono debe tener al menos 7 dígitos.")
            if len(valor_str) > 15:
                raise ValueError("El teléfono no puede exceder 15 dígitos.")
        except ValueError as e:
            raise ClienteInvalidoError(f"Validación de teléfono fallida: {e}") from e
        
        self.__telefono = valor_str

    @property
    def historial_reservas(self):
        """
        MEJORA: Propiedad para acceder al historial de reservas del cliente.
        Proporciona acceso de lectura a las reservas realizadas.
        """
        return self.__historial_reservas.copy()

    def agregar_reserva(self, reserva):
        """
        MEJORA: Método para registrar una reserva en el historial del cliente.
        Esto permite rastrear todas las reservas asociadas con este cliente.
        """
        self.__historial_reservas.append(reserva)

    def obtener_total_gasto(self):
        """
        MEJORA: Método que calcula el gasto total del cliente en todas sus reservas.
        Útil para análisis y reportes de clientes frecuentes.
        """
        if not self.__historial_reservas:
            return 0
        return sum(reserva.servicio.calcular_costo() for reserva in self.__historial_reservas)

    def mostrar_informacion(self):
        """Implementación del método abstracto de la clase Entidad"""
        return f"Cliente: {self.nombre} | Doc: {self.documento} | Correo: {self.correo} | Tel: {self.telefono}"

    def __str__(self):
        return self.mostrar_informacion()
