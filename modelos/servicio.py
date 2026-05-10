from abc import ABC, abstractmethod
from modelos.excepciones import DatosInvalidosError

class Servicio(ABC):
    """
    Clase abstracta que define la interfaz para todos los servicios del sistema.
    
    MEJORA: Se agregó validación del costo_base en el constructor para garantizar
    que ningún servicio tenga un costo inválido (menor o igual a 0).
    
    PARÁMETROS:
    - nombre: Nombre del servicio
    - costo_base: Costo base (debe ser > 0)
    - disponible: Booleano que indica si el servicio está disponible para reservar
    
    PRINCIPIOS APLICADOS:
    - Abstracción: Métodos abstractos que obligan a subclases a implementarlos
    - Validación de datos de entrada en el constructor
    - Encapsulación de parámetros
    """
    
    def __init__(self, nombre, costo_base, disponible=True):
        # MEJORA: Validación de costo_base en el constructor
        try:
            if costo_base <= 0:
                raise ValueError(
                    f"El costo base debe ser mayor a 0. Costo recibido: {costo_base}"
                )
            if not isinstance(disponible, bool):
                raise ValueError(
                    f"El parámetro 'disponible' debe ser booleano. Recibido: {type(disponible).__name__}"
                )
        except ValueError as e:
            # Encadenamiento de excepciones para mejor contexto
            raise DatosInvalidosError(f"Validación de servicio fallida: {e}") from e
        
        self.nombre = nombre
        self.costo_base = costo_base
        self.disponible = disponible

    @abstractmethod
    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        """
        MEJORA: Método abstracto con parámetros opcionales por defecto.
        
        Calcula el costo del servicio con las siguientes variantes:
        - Sin impuesto ni descuento: calcular_costo()
        - Con impuesto: calcular_costo(impuesto=0.19)
        - Con descuento: calcular_costo(descuento=0.10)
        - Con ambos: calcular_costo(impuesto=0.19, descuento=0.10)
        
        PARÁMETROS:
        - impuesto: Tasa de impuesto a aplicar (ej: 0.19 para 19% de IVA)
        - descuento: Tasa de descuento a aplicar (ej: 0.10 para 10% de descuento)
        
        RETORNA:
        - Costo total como número decimal
        
        NOTA: Esta es una función SOBRECARGADA (por parámetros opcionales)
        que permite múltiples formas de invocación.
        """
        pass

    @abstractmethod
    def describir_servicio(self):
        """
        Retorna una descripción legible del servicio.
        Cada subclase implementa su propia descripción.
        """
        pass

    @abstractmethod
    def validar_servicio(self):
        """
        Valida que los parámetros específicos del servicio sean correctos.
        Cada subclase valida sus propios atributos.
        """
        pass
