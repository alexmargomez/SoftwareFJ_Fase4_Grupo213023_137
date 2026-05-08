class SistemaError(Exception):
    """Clase base para excepciones del sistema."""
    pass

class ClienteInvalidoError(SistemaError):
    """Lanzada cuando un cliente no cumple con las validaciones."""
    pass

class ServicioNoDisponibleError(SistemaError):
    """Lanzada cuando se intenta reservar un servicio no disponible."""
    pass

class ReservaError(SistemaError):
    """Lanzada cuando hay un error en el proceso de reserva."""
    pass

class DatosInvalidosError(SistemaError):
    """Lanzada cuando se proporcionan datos de entrada no válidos."""
    pass
