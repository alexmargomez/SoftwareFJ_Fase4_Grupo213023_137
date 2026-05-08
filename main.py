from modelos.cliente import Cliente
from modelos.reserva import Reserva
from modelos.excepciones import SistemaError
from servicios.reserva_sala import ReservaSala
from servicios.alquiler_equipo import AlquilerEquipo
from servicios.asesoria import AsesoriaEspecializada
from utils.logger import logger
import traceback

def ejecutar_simulacion():
    print("=== Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ ===")
    
    # 1. Crear clientes válidos
    try:
        cliente1 = Cliente("Juan Perez", "12345678", "juan@mail.com", "3001234567")
        cliente2 = Cliente("Maria Lopez", "87654321", "maria@mail.com", "3109876543")
        logger.info("Clientes válidos creados exitosamente.")
    except SistemaError as e:
        logger.error(f"Error al crear clientes iniciales: {e}")

    # 2. Operación 1: Reserva de Sala Exitosa
    print("\n[Operación 1: Reserva de Sala Exitosa]")
    try:
        sala = ReservaSala("Sala de Juntas A", 50000, 10, 3)
        reserva1 = Reserva(cliente1, sala, 3)
        reserva1.procesar_reserva()
    except SistemaError as e:
        print(f"Error esperado: {e}")

    # 3. Operación 2: Alquiler de Equipo Exitoso (con impuesto)
    print("\n[Operación 2: Alquiler de Equipo Exitoso con Impuesto]")
    try:
        equipo = AlquilerEquipo("Laptop Dell", 20000, "Portátil", 5)
        reserva2 = Reserva(cliente2, equipo, 5)
        reserva2.procesar_reserva()
        costo_con_impuesto = equipo.calcular_costo(impuesto=0.19)
        print(f"Costo total con IVA (19%): ${costo_con_impuesto:.2f}")
    except SistemaError as e:
        print(f"Error: {e}")

    # 4. Operación 3: Asesoría Exitosa (con descuento)
    print("\n[Operación 3: Asesoría Exitosa con Descuento]")
    try:
        asesoria = AsesoriaEspecializada("Consultoría IT", 80000, "Ing. Carlos", 2)
        reserva3 = Reserva(cliente1, asesoria, 2)
        reserva3.procesar_reserva()
        costo_con_descuento = asesoria.calcular_costo(descuento=0.10)
        print(f"Costo total con descuento (10%): ${costo_con_descuento:.2f}")
    except SistemaError as e:
        print(f"Error: {e}")

    # 5. Operación 4: Intento de crear cliente con nombre vacío
    print("\n[Operación 4: Cliente con nombre vacío]")
    try:
        Cliente("", "111", "error@mail.com", "1234567")
    except SistemaError as e:
        print(f"Capturado: {e}")
        logger.warning(f"Validación fallida: {e}")

    # 6. Operación 5: Intento de crear cliente con documento no numérico
    print("\n[Operación 5: Cliente con documento no numérico]")
    try:
        Cliente("Pedro", "ABC123", "pedro@mail.com", "1234567")
    except SistemaError as e:
        print(f"Capturado: {e}")
        logger.warning(f"Validación fallida: {e}")

    # 7. Operación 6: Intento de crear cliente con correo inválido
    print("\n[Operación 6: Cliente con correo inválido]")
    try:
        Cliente("Pedro", "12345", "correo-invalido", "1234567")
    except SistemaError as e:
        print(f"Capturado: {e}")
        logger.warning(f"Validación fallida: {e}")

    # 8. Operación 7: Servicio no disponible
    print("\n[Operación 7: Reserva de servicio no disponible]")
    try:
        sala_ocupada = ReservaSala("Sala B", 40000, 5, 2, disponible=False)
        reserva4 = Reserva(cliente2, sala_ocupada, 2)
        reserva4.procesar_reserva()
    except SistemaError as e:
        print(f"Capturado: {e}")

    # 9. Operación 8: Datos de servicio inválidos (Capacidad 0)
    print("\n[Operación 8: Datos de servicio inválidos (Capacidad 0)]")
    try:
        sala_invalida = ReservaSala("Sala C", 30000, 0, 1)
        reserva5 = Reserva(cliente1, sala_invalida, 1)
        reserva5.procesar_reserva()
    except SistemaError as e:
        print(f"Capturado: {e}")

    # 10. Operación 9: Cancelación de reserva
    print("\n[Operación 9: Cancelación de reserva]")
    try:
        reserva1.cancelar()
        print(f"Estado de reserva 1: {reserva1.estado}")
    except SistemaError as e:
        print(f"Error: {e}")

    # 11. Operación 10: Re-confirmar reserva ya confirmada (Error)
    print("\n[Operación 10: Re-confirmar reserva ya confirmada o cancelada]")
    try:
        reserva1.confirmar()
    except SistemaError as e:
        print(f"Capturado: {e}")

    # 12. Demostración de manejo (try/except/else/finally)
    print("\n[Operación Extra: Demostración de try/except/else/finally]")
    try:
        print("Intentando crear una reserva perfecta...")
        s = ReservaSala("Auditorio", 100000, 50, 4)
        r = Reserva(cliente2, s, 4)
        r.validar_datos()
    except SistemaError as e:
        print(f"Ocurrió un error: {e}")
    else:
        print("No hubo errores en la validación.")
        r.confirmar()
    finally:
        print("Limpieza de recursos (simulada). La ejecución continúa.")

    print("\n=== Simulación Finalizada ===")
    print("Revise el archivo 'logs/eventos.log' para el detalle técnico.")

if __name__ == "__main__":
    try:
        ejecutar_simulacion()
    except Exception as e:
        # Este bloque asegura que el programa NUNCA se detenga abruptamente
        print(f"Error crítico no controlado: {e}")
        logger.critical(f"Error fatal: {e}\n{traceback.format_exc()}")
