"""
SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS - SOFTWARE FJ
FASE 4 - GRUPO 213023

MEJORAS IMPLEMENTADAS (Mayo 2026):
==================================

1. GESTIÓN DE COLECCIONES:
   - Nuevo módulo: modelos/gestor.py (GestorSistema con patrón Singleton)
   - Mantiene listas centralizadas de clientes, servicios y reservas
   - Permite búsqueda, filtrado y reportes

2. VALIDACIONES MEJORADAS:
   - Cliente: Nombre mín 3 caracteres, Documento mín 5 dígitos, Teléfono máx 15 dígitos
   - Servicio: Validación de costo_base > 0 en constructor
   - Servicio: Validación de tipo booleano para 'disponible'
   - Prevención de documentos duplicados

3. ENCADENAMIENTO DE EXCEPCIONES:
   - Uso de 'raise ... from e' en validaciones
   - Mejor contexto de error para debugging

4. try/except/else EXPLÍCITO:
   - Implementado en Reserva.procesar_reserva()
   - Bloque ELSE ejecuta solo si validación fue exitosa
   - Bloque FINALLY siempre ejecuta

5. TRAZABILIDAD:
   - Cada reserva tiene ID único (UUID)
   - Historial de cambios de estado con timestamp
   - Historial de reservas por cliente

6. REPORTES Y ESTADÍSTICAS:
   - Método mostrar_resumen() del GestorSistema
   - Cálculo de ingresos totales
   - Estadísticas de reservas confirmadas/canceladas
"""

from modelos.cliente import Cliente
from modelos.reserva import Reserva
from modelos.excepciones import SistemaError
from servicios.reserva_sala import ReservaSala
from servicios.alquiler_equipo import AlquilerEquipo
from servicios.asesoria import AsesoriaEspecializada
from modelos.gestor import GestorSistema
from utils.logger import logger
import traceback

# MEJORA: Instancia única del gestor del sistema (Patrón Singleton)
gestor = GestorSistema()


def ejecutar_simulacion():
    """
    FUNCIÓN PRINCIPAL: Ejecuta 15+ operaciones para demostrar la robustez del sistema.
    Incluye casos de éxito, validaciones fallidas y manejo de excepciones.
    """
    
    print("="*80)
    print("  SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS - SOFTWARE FJ")
    print("="*80)
    
    # ==================== SECCIÓN 1: CREACIÓN DE CLIENTES ====================
    print("\n[SECCIÓN 1: CREACIÓN Y REGISTRO DE CLIENTES]")
    print("-" * 80)
    
    # Operación 1: Clientes válidos
    print("\n✓ Operación 1: Crear clientes válidos")
    try:
        cliente1 = Cliente("Juan Perez", "12345678", "juan@mail.com", "3001234567")
        cliente2 = Cliente("Maria Lopez", "87654321", "maria@mail.com", "3109876543")
        
        # MEJORA: Registrar en el gestor
        gestor.registrar_cliente(cliente1)
        gestor.registrar_cliente(cliente2)
        
        logger.info("Clientes válidos creados y registrados exitosamente.")
        print(f"  ✅ {cliente1.mostrar_informacion()}")
        print(f"  ✅ {cliente2.mostrar_informacion()}")
    except SistemaError as e:
        logger.error(f"Error al crear clientes: {e}")
        print(f"  ❌ Error: {e}")

    # Operación 2: Intento de registrar cliente duplicado (documento ya existe)
    print("\n✓ Operación 2: Intentar registrar cliente con documento duplicado")
    try:
        cliente_duplicado = Cliente("Carlos Otro", "12345678", "carlos@mail.com", "3005554444")
        # MEJORA: GestorSistema detecta documento duplicado
        gestor.registrar_cliente(cliente_duplicado)
    except SistemaError as e:
        logger.warning(f"Documento duplicado detectado: {e}")
        print(f"  ✅ Validación correcta: {e}")

    # Operación 3: Cliente con nombre muy corto
    print("\n✓ Operación 3: Intento de crear cliente con nombre muy corto")
    try:
        Cliente("AB", "99999999", "short@mail.com", "3001234567")
    except SistemaError as e:
        logger.warning(f"Nombre rechazado: {e}")
        print(f"  ✅ Validación correcta: {e}")

    # Operación 4: Cliente con documento muy corto
    print("\n✓ Operación 4: Intento de crear cliente con documento muy corto")
    try:
        Cliente("Pedro", "123", "pedro@mail.com", "3001234567")
    except SistemaError as e:
        logger.warning(f"Documento corto rechazado: {e}")
        print(f"  ✅ Validación correcta: {e}")

    # Operación 5: Cliente con teléfono inválido (muy largo)
    print("\n✓ Operación 5: Intento de crear cliente con teléfono excesivamente largo")
    try:
        Cliente("Ana", "55555555", "ana@mail.com", "300123456789012345")  # > 15 dígitos
    except SistemaError as e:
        logger.warning(f"Teléfono rechazado: {e}")
        print(f"  ✅ Validación correcta: {e}")

    # ==================== SECCIÓN 2: CREACIÓN DE SERVICIOS ====================
    print("\n[SECCIÓN 2: CREACIÓN Y REGISTRO DE SERVICIOS]")
    print("-" * 80)

    # Operación 6: Servicios válidos
    print("\n✓ Operación 6: Crear y registrar servicios válidos")
    try:
        sala = ReservaSala("Sala de Juntas A", 50000, 10, 3)
        equipo = AlquilerEquipo("Laptop Dell", 20000, "Portátil", 5)
        asesoria = AsesoriaEspecializada("Consultoría IT", 80000, "Ing. Carlos", 2)
        
        # MEJORA: Registrar servicios en el gestor
        gestor.registrar_servicio(sala)
        gestor.registrar_servicio(equipo)
        gestor.registrar_servicio(asesoria)
        
        logger.info("Servicios registrados exitosamente.")
        print(f"  ✅ {sala.describir_servicio()}")
        print(f"  ✅ {equipo.describir_servicio()}")
        print(f"  ✅ {asesoria.describir_servicio()}")
    except SistemaError as e:
        logger.error(f"Error al crear servicios: {e}")
        print(f"  ❌ Error: {e}")

    # Operación 7: Intento de crear servicio con costo inválido
    print("\n✓ Operación 7: Intento de crear servicio con costo base inválido (<= 0)")
    try:
        # MEJORA: Validación mejorada de costo_base
        sala_invalida = ReservaSala("Sala Gratis", 0, 10, 3)
    except SistemaError as e:
        logger.warning(f"Costo inválido rechazado: {e}")
        print(f"  ✅ Validación correcta: {e}")

    # ==================== SECCIÓN 3: PROCESAMIENTO DE RESERVAS ====================
    print("\n[SECCIÓN 3: PROCESAMIENTO DE RESERVAS]")
    print("-" * 80)

    # Operación 8: Reserva exitosa con cálculo de costo
    print("\n✓ Operación 8: Reserva exitosa con cálculo de costo")
    try:
        reserva1 = Reserva(cliente1, sala, 3)
        # MEJORA: procesar_reserva usa try/except/else/finally
        reserva1.procesar_reserva()
        # MEJORA: Registrar reserva procesada en el gestor
        gestor.registrar_reserva(reserva1)
    except SistemaError as e:
        logger.error(f"Error al procesar reserva: {e}")
        print(f"  ❌ Error: {e}")

    # Operación 9: Alquiler de equipo con cálculo de impuesto
    print("\n✓ Operación 9: Alquiler de equipo con cálculo de impuesto (IVA 19%)")
    try:
        reserva2 = Reserva(cliente2, equipo, 5)
        reserva2.procesar_reserva()
        # MEJORA: Cálculo de costo con impuesto (método sobrecargado)
        costo_con_impuesto = equipo.calcular_costo(impuesto=0.19)
        print(f"       Costo con IVA (19%): ${costo_con_impuesto:,.2f}")
        gestor.registrar_reserva(reserva2)
    except SistemaError as e:
        logger.error(f"Error: {e}")
        print(f"  ❌ Error: {e}")

    # Operación 10: Asesoría con descuento
    print("\n✓ Operación 10: Asesoría con cálculo de descuento (10%)")
    try:
        reserva3 = Reserva(cliente1, asesoria, 2)
        reserva3.procesar_reserva()
        # MEJORA: Cálculo de costo con descuento
        costo_con_descuento = asesoria.calcular_costo(descuento=0.10)
        print(f"       Costo con descuento (10%): ${costo_con_descuento:,.2f}")
        gestor.registrar_reserva(reserva3)
    except SistemaError as e:
        logger.error(f"Error: {e}")
        print(f"  ❌ Error: {e}")

    # Operación 11: Intento de reserva de servicio no disponible
    print("\n✓ Operación 11: Intento de reservar servicio no disponible")
    try:
        sala_ocupada = ReservaSala("Sala B", 40000, 5, 2, disponible=False)
        reserva4 = Reserva(cliente2, sala_ocupada, 2)
        reserva4.procesar_reserva()
    except SistemaError as e:
        logger.warning(f"Servicio no disponible: {e}")
        print(f"  ✅ Error capturado correctamente: {e}")

    # Operación 12: Intento de reserva con capacidad 0
    print("\n✓ Operación 12: Intento de reserva con datos inválidos (Capacidad 0)")
    try:
        sala_invalida = ReservaSala("Sala C", 30000, 0, 1)
        reserva5 = Reserva(cliente1, sala_invalida, 1)
        reserva5.procesar_reserva()
    except SistemaError as e:
        logger.warning(f"Datos inválidos: {e}")
        print(f"  ✅ Error capturado correctamente: {e}")

    # ==================== SECCIÓN 4: GESTIÓN DE RESERVAS ====================
    print("\n[SECCIÓN 4: GESTIÓN Y CANCELACIÓN DE RESERVAS]")
    print("-" * 80)

    # Operación 13: Cancelación de reserva
    print("\n✓ Operación 13: Cancelar una reserva")
    try:
        reserva1.cancelar()
        print(f"  ✅ Reserva cancelada. Estado actual: {reserva1.estado}")
        # MEJORA: Mostrar historial de cambios
        print(f"  📋 Historial de cambios:")
        for cambio in reserva1.obtener_historial():
            print(f"     - {cambio['fecha']}: {cambio['estado_anterior']} → {cambio['estado_nuevo']} ({cambio['razon']})")
    except SistemaError as e:
        logger.error(f"Error al cancelar: {e}")
        print(f"  ❌ Error: {e}")

    # Operación 14: Intento de re-confirmar reserva ya confirmada
    print("\n✓ Operación 14: Intento de re-confirmar reserva ya confirmada")
    try:
        reserva3.confirmar()
    except SistemaError as e:
        logger.warning(f"No se puede re-confirmar: {e}")
        print(f"  ✅ Error capturado correctamente: {e}")

    # Operación 15: Intento de cancelar reserva ya cancelada
    print("\n✓ Operación 15: Intento de cancelar reserva ya cancelada")
    try:
        reserva1.cancelar()
    except SistemaError as e:
        logger.warning(f"No se puede cancelar dos veces: {e}")
        print(f"  ✅ Error capturado correctamente: {e}")

    # ==================== SECCIÓN 5: BÚSQUEDA Y REPORTES ====================
    print("\n[SECCIÓN 5: BÚSQUEDA Y REPORTES]")
    print("-" * 80)

    # Operación 16: Búsqueda de cliente por documento
    print("\n✓ Operación 16: Buscar cliente por documento")
    try:
        cliente_encontrado = gestor.buscar_cliente_por_documento("12345678")
        if cliente_encontrado:
            print(f"  ✅ Cliente encontrado: {cliente_encontrado.mostrar_informacion()}")
            # MEJORA: Mostrar historial de reservas del cliente
            print(f"  📋 Reservas del cliente:")
            reservas_cliente = cliente_encontrado.historial_reservas
            if reservas_cliente:
                for res in reservas_cliente:
                    print(f"     - {res.servicio.nombre}: ${res.servicio.calcular_costo():,.2f} (Estado: {res.estado})")
                print(f"     Total gastado: ${cliente_encontrado.obtener_total_gasto():,.2f}")
            else:
                print(f"     (Sin reservas)")
    except Exception as e:
        logger.error(f"Error en búsqueda: {e}")

    # Operación 17: Listar servicios disponibles
    print("\n✓ Operación 17: Listar servicios disponibles")
    try:
        servicios_disponibles = gestor.obtener_servicios_disponibles()
        print(f"  ✅ Servicios disponibles ({len(servicios_disponibles)}):")
        for svc in servicios_disponibles:
            print(f"     - {svc.describir_servicio()}")
    except Exception as e:
        logger.error(f"Error: {e}")

    # ==================== SECCIÓN 6: DEMOSTRACIÓN DE try/except/else/finally ====================
    print("\n[SECCIÓN 6: DEMOSTRACIÓN DE try/except/else/finally]")
    print("-" * 80)
    print("\n✓ Operación 18: Validación con flujo try/except/else/finally")
    try:
        print("  → Intentando crear una reserva perfecta...")
        s = ReservaSala("Auditorio Premium", 100000, 50, 4)
        r = Reserva(cliente2, s, 4)
        r.validar_datos()
        print("  → Validación en el bloque try: COMPLETADA")
        
    except SistemaError as e:
        print(f"  ❌ Ocurrió un error en el except: {e}")
        
    else:
        # MEJORA: Este bloque SOLO ejecuta si NO hay excepción
        print("  → Bloque ELSE ejecutado: No hubo errores en la validación")
        r.confirmar()
        print("  ✅ Reserva confirmada automáticamente en el else")
        
    finally:
        # Este bloque SIEMPRE ejecuta
        print("  → Bloque FINALLY ejecutado: Limpieza de recursos completada")

    # ==================== SECCIÓN 7: RESUMEN DEL SISTEMA ====================
    print("\n[SECCIÓN 7: RESUMEN Y ESTADÍSTICAS DEL SISTEMA]")
    print("-" * 80)
    
    # MEJORA: Mostrar resumen del gestor
    gestor.mostrar_resumen()
    
    # Detalles adicionales
    print("\n📊 ESTADÍSTICAS DETALLADAS:")
    print(f"  • Clientes registrados: {gestor.cantidad_clientes()}")
    print(f"  • Servicios disponibles: {len(gestor.obtener_servicios_disponibles())}")
    print(f"  • Total de reservas: {gestor.cantidad_reservas()}")
    print(f"  • Reservas confirmadas: {len(gestor.obtener_reservas_confirmadas())}")
    print(f"  • Reservas canceladas: {len(gestor.obtener_reservas_canceladas())}")

    print("\n" + "="*80)
    print("✅ SIMULACIÓN COMPLETADA CON ÉXITO")
    print("📄 Revise el archivo 'logs/eventos.log' para el detalle técnico de todas las operaciones")
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        ejecutar_simulacion()
    except Exception as e:
        # MEJORA: Manejo de errores críticos no controlados
        print(f"\n❌ ERROR CRÍTICO NO CONTROLADO: {e}")
        logger.critical(f"Error fatal no manejado:\n{traceback.format_exc()}")
        print("\n📄 Se ha registrado el error en logs/eventos.log")
