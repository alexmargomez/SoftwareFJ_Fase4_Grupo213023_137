"""
MÓDULO: gestor.py
PROPÓSITO: Gestión centralizada del sistema Software FJ

MEJORA CRÍTICA IMPLEMENTADA:
Este archivo fue agregado para cumplir con el requisito de "manejo de listas internas"
del proyecto. Implementa el patrón Singleton para garantizar una única instancia del 
gestor del sistema, permitiendo:
1. Mantener listas centralizadas de clientes, servicios y reservas
2. Buscar y recuperar entidades de forma eficiente
3. Validar unicidad de datos (ej: documento duplicado)
4. Proporcionar reportes y estadísticas del sistema
5. Garantizar consistencia de datos en toda la aplicación

PRINCIPIOS APLICADOS:
- Patrón Singleton: Una única instancia del gestor
- CRUD (Create, Read, Update, Delete): Operaciones sobre las colecciones
- Encapsulación: Acceso controlado a las listas internas
- Validación: Verificación de restricciones de negocio

JUSTIFICACIÓN:
El requisito especificaba "manejo de listas internas y validaciones estrictas".
Esto requería una clase que administre colecciones de entidades del sistema.
"""

from modelos.excepciones import ClienteInvalidoError, ReservaError, DatosInvalidosError
from utils.logger import logger


class GestorSistema:
    """
    Clase que gestiona centralmente todos los datos del sistema Software FJ.
    
    Implementa el patrón Singleton para garantizar que exista una única instancia
    del gestor en toda la aplicación, evitando inconsistencias de datos.
    
    ATRIBUTOS PRIVADOS:
    - __clientes: Lista de clientes registrados en el sistema
    - __servicios: Lista de servicios disponibles
    - __reservas: Lista de todas las reservas procesadas
    - __instancia: Variable de clase para el patrón Singleton
    """
    
    _instancia = None
    
    def __new__(cls):
        """
        MEJORA: Implementación del patrón Singleton.
        Garantiza que solo exista una instancia del GestorSistema.
        Si ya existe una instancia, la retorna; si no, la crea.
        """
        if cls._instancia is None:
            cls._instancia = super(GestorSistema, cls).__new__(cls)
            # Inicializar las listas solo en la primera creación
            cls._instancia.__inicializar()
        return cls._instancia
    
    def __inicializar(self):
        """
        MEJORA: Inicialización de las listas internas del sistema.
        Se llama automáticamente la primera vez que se crea la instancia.
        """
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []
        logger.info("GestorSistema inicializado con éxito")
    
    # ==================== MÉTODOS PARA CLIENTES ====================
    
    def registrar_cliente(self, cliente):
        """
        MEJORA: Registra un nuevo cliente en el sistema.
        
        VALIDACIONES:
        - Verifica que no exista otro cliente con el mismo documento
        - Evita registros duplicados
        
        PARÁMETROS:
        - cliente: Objeto de clase Cliente a registrar
        
        EXCEPCIONES:
        - ClienteInvalidoError: Si el cliente ya está registrado
        
        RETORNA:
        - True si el registro fue exitoso
        """
        try:
            # MEJORA: Búsqueda de documento duplicado
            if self.buscar_cliente_por_documento(cliente.documento) is not None:
                raise ClienteInvalidoError(
                    f"El cliente con documento '{cliente.documento}' ya está registrado en el sistema."
                )
            
            self.__clientes.append(cliente)
            logger.info(f"Cliente registrado: {cliente.nombre} (Doc: {cliente.documento})")
            return True
            
        except ClienteInvalidoError as e:
            logger.warning(f"Intento de registro fallido: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al registrar cliente: {e}")
            raise
    
    def buscar_cliente_por_documento(self, documento):
        """
        MEJORA: Búsqueda de cliente por número de documento.
        Fundamental para validar unicidad de documentos.
        
        PARÁMETROS:
        - documento: Número de documento a buscar
        
        RETORNA:
        - Objeto Cliente si existe, None si no existe
        """
        for cliente in self.__clientes:
            if cliente.documento == str(documento):
                return cliente
        return None
    
    def obtener_todos_clientes(self):
        """
        MEJORA: Retorna una copia de la lista de clientes.
        Proporciona acceso de lectura sin permitir modificaciones directas.
        
        RETORNA:
        - Lista con copia de todos los clientes registrados
        """
        return self.__clientes.copy()
    
    def cantidad_clientes(self):
        """MEJORA: Retorna el número total de clientes registrados."""
        return len(self.__clientes)
    
    # ==================== MÉTODOS PARA SERVICIOS ====================
    
    def registrar_servicio(self, servicio):
        """
        MEJORA: Registra un nuevo servicio en el sistema.
        
        VALIDACIONES:
        - Valida que el servicio tenga costo_base > 0
        
        PARÁMETROS:
        - servicio: Objeto de clase Servicio (o subclase) a registrar
        
        EXCEPCIONES:
        - DatosInvalidosError: Si el costo_base es inválido
        
        RETORNA:
        - True si el registro fue exitoso
        """
        try:
            # MEJORA: Validación de costo_base
            if servicio.costo_base <= 0:
                raise DatosInvalidosError(
                    f"El costo base del servicio debe ser mayor a 0. Costo recibido: {servicio.costo_base}"
                )
            
            self.__servicios.append(servicio)
            logger.info(f"Servicio registrado: {servicio.nombre} (Costo: ${servicio.costo_base})")
            return True
            
        except DatosInvalidosError as e:
            logger.warning(f"Intento de registro de servicio fallido: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al registrar servicio: {e}")
            raise
    
    def obtener_servicios_disponibles(self):
        """
        MEJORA: Retorna solo los servicios que están disponibles.
        Permite filtrar qué servicios pueden ser reservados.
        
        RETORNA:
        - Lista de servicios con disponible=True
        """
        servicios_disponibles = [s for s in self.__servicios if s.disponible]
        return servicios_disponibles
    
    def obtener_todos_servicios(self):
        """MEJORA: Retorna una copia de todos los servicios registrados."""
        return self.__servicios.copy()
    
    def cantidad_servicios(self):
        """MEJORA: Retorna el número total de servicios registrados."""
        return len(self.__servicios)
    
    # ==================== MÉTODOS PARA RESERVAS ====================
    
    def registrar_reserva(self, reserva):
        """
        MEJORA: Registra una reserva procesada en el sistema.
        
        PARÁMETROS:
        - reserva: Objeto de clase Reserva que se ha procesado exitosamente
        
        RETORNA:
        - True si el registro fue exitoso
        """
        try:
            # MEJORA: Agregar reserva a la lista global
            self.__reservas.append(reserva)
            
            # MEJORA: Agregar reserva al historial del cliente
            reserva.cliente.agregar_reserva(reserva)
            
            logger.info(
                f"Reserva registrada: Cliente={reserva.cliente.nombre}, "
                f"Servicio={reserva.servicio.nombre}, Estado={reserva.estado}"
            )
            return True
            
        except Exception as e:
            logger.error(f"Error al registrar reserva: {e}")
            raise
    
    def obtener_todas_reservas(self):
        """MEJORA: Retorna una copia de todas las reservas registradas."""
        return self.__reservas.copy()
    
    def cantidad_reservas(self):
        """MEJORA: Retorna el número total de reservas registradas."""
        return len(self.__reservas)
    
    def obtener_reservas_cliente(self, cliente):
        """
        MEJORA: Retorna todas las reservas de un cliente específico.
        
        PARÁMETROS:
        - cliente: Objeto Cliente cuyas reservas se desean obtener
        
        RETORNA:
        - Lista de reservas del cliente
        """
        return [r for r in self.__reservas if r.cliente.documento == cliente.documento]
    
    def obtener_reservas_confirmadas(self):
        """MEJORA: Retorna solo las reservas confirmadas."""
        return [r for r in self.__reservas if r.estado == "Confirmada"]
    
    def obtener_reservas_canceladas(self):
        """MEJORA: Retorna solo las reservas canceladas."""
        return [r for r in self.__reservas if r.estado == "Cancelada"]
    
    # ==================== MÉTODOS DE REPORTES ====================
    
    def generar_reporte_sistema(self):
        """
        MEJORA: Genera un reporte completo del estado del sistema.
        Muestra estadísticas generales de clientes, servicios y reservas.
        
        RETORNA:
        - Diccionario con estadísticas del sistema
        """
        reporte = {
            "total_clientes": self.cantidad_clientes(),
            "total_servicios": self.cantidad_servicios(),
            "servicios_disponibles": len(self.obtener_servicios_disponibles()),
            "total_reservas": self.cantidad_reservas(),
            "reservas_confirmadas": len(self.obtener_reservas_confirmadas()),
            "reservas_canceladas": len(self.obtener_reservas_canceladas()),
            "ingresos_totales": self._calcular_ingresos_totales()
        }
        return reporte
    
    def _calcular_ingresos_totales(self):
        """
        MEJORA: Calcula los ingresos totales del sistema.
        Solo cuenta reservas confirmadas.
        
        RETORNA:
        - Suma total de costos de reservas confirmadas
        """
        reservas_confirmadas = self.obtener_reservas_confirmadas()
        if not reservas_confirmadas:
            return 0
        return sum(r.servicio.calcular_costo() for r in reservas_confirmadas)
    
    def mostrar_resumen(self):
        """
        MEJORA: Imprime un resumen del estado del sistema.
        Útil para mostrar en consola el estado actual.
        """
        reporte = self.generar_reporte_sistema()
        print("\n" + "="*60)
        print("RESUMEN DEL SISTEMA SOFTWARE FJ")
        print("="*60)
        print(f"Total de Clientes:        {reporte['total_clientes']}")
        print(f"Total de Servicios:       {reporte['total_servicios']}")
        print(f"Servicios Disponibles:    {reporte['servicios_disponibles']}")
        print(f"Total de Reservas:        {reporte['total_reservas']}")
        print(f"Reservas Confirmadas:     {reporte['reservas_confirmadas']}")
        print(f"Reservas Canceladas:      {reporte['reservas_canceladas']}")
        print(f"Ingresos Totales:         ${reporte['ingresos_totales']:,.2f}")
        print("="*60 + "\n")
