from modelos.excepciones import ReservaError, ServicioNoDisponibleError
from utils.logger import logger
from datetime import datetime
import uuid

class Reserva:
    """
    Clase que representa una reserva de servicio en el sistema Software FJ.
    
    MEJORAS IMPLEMENTADAS:
    1. Agregado ID único (UUID) para identificar cada reserva de forma global
    2. Agregada fecha_creación para registrar cuándo se creó la reserva
    3. Agregado historial_cambios para rastrear cambios de estado
    4. Implementado try/except/else explícitamente en procesar_reserva()
    5. Mejorado el manejo de excepciones con encadenamiento
    
    PRINCIPIOS APLICADOS:
    - Trazabilidad completa de operaciones
    - Manejo robusto de excepciones con try/except/else/finally
    - Historial de auditoría de cambios
    """
    
    def __init__(self, cliente, servicio, duracion):
        self.id = str(uuid.uuid4())  # MEJORA: ID único para cada reserva
        self.fecha_creacion = datetime.now()  # MEJORA: Registro de fecha/hora
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        # MEJORA: Historial de cambios de estado con timestamp
        self.__historial_cambios = [{
            'fecha': self.fecha_creacion,
            'estado_anterior': None,
            'estado_nuevo': "Pendiente",
            'razon': "Creación de reserva"
        }]

    def _registrar_cambio(self, estado_nuevo, razon=""):
        """
        MEJORA: Método privado para registrar cambios de estado.
        Mantiene un historial completo de transiciones de estado.
        
        PARÁMETROS:
        - estado_nuevo: Nuevo estado de la reserva
        - razon: Razón del cambio (para auditoría)
        """
        self.__historial_cambios.append({
            'fecha': datetime.now(),
            'estado_anterior': self.estado,
            'estado_nuevo': estado_nuevo,
            'razon': razon
        })

    def obtener_historial(self):
        """MEJORA: Retorna una copia del historial de cambios."""
        return self.__historial_cambios.copy()

    def validar_datos(self):
        """
        Valida que los datos de la reserva sean correctos.
        
        MEJORA: Se mejoró la validación de cliente para manejar None de forma segura.
        """
        try:
            # MEJORA: Validación más robusta del cliente
            if self.cliente is None:
                raise ReservaError("Cliente no válido (None).")
            
            # Verificar que el cliente tiene al menos el atributo nombre
            if not hasattr(self.cliente, 'nombre'):
                raise ReservaError("Cliente no tiene atributo 'nombre'.")
            
            if self.servicio is None:
                raise ReservaError("Servicio no válido (None).")
            
            if self.duracion <= 0:
                raise ValueError("La duración debe ser mayor a 0.")
            
            # MEJORA: Se separa la validación de disponibilidad
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self.servicio.nombre}' no está disponible para reservar."
                )
            
            # MEJORA: Se llama a validación específica del servicio
            self.servicio.validar_servicio()
            
        except ValueError as e:
            # Encadenamiento de excepciones para datos inválidos
            raise ReservaError(f"Validación de datos fallida: {e}") from e
        except (ReservaError, ServicioNoDisponibleError):
            # Re-lanzar excepciones del sistema
            raise

    def confirmar(self):
        """
        Confirma una reserva pendiente.
        Solo puede confirmar si la reserva está en estado "Pendiente".
        """
        if self.estado == "Pendiente":
            self.estado = "Confirmada"
            self._registrar_cambio("Confirmada", "Confirmación exitosa de reserva")
            logger.info(f"Reserva {self.id} confirmada para {self.cliente.nombre} - Servicio: {self.servicio.nombre}")
        else:
            raise ReservaError(f"No se puede confirmar una reserva en estado: {self.estado}")

    def cancelar(self):
        """
        Cancela una reserva que no esté ya cancelada.
        """
        if self.estado != "Cancelada":
            estado_anterior = self.estado
            self.estado = "Cancelada"
            self._registrar_cambio("Cancelada", f"Cancelación desde estado {estado_anterior}")
            logger.info(f"Reserva {self.id} cancelada para {self.cliente.nombre} - Servicio: {self.servicio.nombre}")
        else:
            raise ReservaError("La reserva ya está cancelada.")

    def procesar_reserva(self):
        """
        MEJORA: Procesamiento completo de reserva con try/except/else/finally explícitamente implementado.
        
        FLUJO:
        - TRY: Intenta validar y confirmar la reserva
        - EXCEPT: Maneja diferentes tipos de errores
        - ELSE: Ejecuta solo si NO hubo excepción (confirmación exitosa)
        - FINALLY: Siempre ejecuta (limpieza/logging)
        
        EXCEPCIONES MANEJADAS:
        - ReservaError: Errores específicos de reserva
        - ServicioNoDisponibleError: Servicio no disponible
        - Exception: Cualquier otro error inesperado
        """
        try:
            # BLOQUE TRY: Intenta validar y procesar la reserva
            logger.info(
                f"Iniciando procesamiento de reserva {self.id} para "
                f"{self.cliente.nombre if self.cliente else 'Cliente desconocido'}"
            )
            
            # Validar datos
            self.validar_datos()
            
            # Si la validación pasó, continuar al bloque ELSE
            
        except ServicioNoDisponibleError as e:
            # MANEJO ESPECÍFICO: Servicio no disponible
            logger.error(f"Servicio no disponible para reserva {self.id}: {e}")
            print(f"❌ Error de disponibilidad: {e}")
            raise e
            
        except ReservaError as e:
            # MANEJO ESPECÍFICO: Errores de reserva
            logger.error(f"Error en reserva {self.id}: {e}")
            print(f"❌ Error en la reserva: {e}")
            raise e
            
        except Exception as e:
            # MANEJO GENÉRICO: Cualquier excepción no prevista
            logger.critical(f"Error inesperado al procesar reserva {self.id}: {e}")
            print(f"❌ Error crítico inesperado: {e}")
            raise ReservaError("Error interno al procesar la reserva.") from e
            
        else:
            # BLOQUE ELSE: Solo ejecuta si NO hubo excepción en el try
            # MEJORA: Confirmación automática y mensaje de éxito
            try:
                self.confirmar()
                costo = self.servicio.calcular_costo()
                print(
                    f"✅ Reserva procesada exitosamente:\n"
                    f"   - {self.servicio.describir_servicio()}\n"
                    f"   - Costo: ${costo:,.2f}\n"
                    f"   - Estado: {self.estado}"
                )
            except Exception as e:
                logger.error(f"Error al confirmar reserva: {e}")
                raise
                
        finally:
            # BLOQUE FINALLY: Siempre ejecuta (limpieza)
            # MEJORA: Logging de cierre de proceso
            logger.debug(
                f"Fin del intento de procesamiento de reserva {self.id} - "
                f"Estado final: {self.estado}"
            )
