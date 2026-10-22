# funciones.py
# Aquí están las funciones que organizan la partida y muestran los mensajes.

from variables import TAMANO_TABLERO


def imprimir_bienvenida():
    print("=" * 46)
    print("           HUNDIR LA FLOTA")
    print("=" * 46)
    print("Juegas contra la máquina en un tablero de 10 x 10.")
    print("Los barcos se colocan aleatoriamente al comenzar.")
    print("Si aciertas, puedes volver a disparar. Si fallas, juega la máquina.")
    print()
    print("SÍMBOLOS:")
    print("B = barco propio sin tocar")
    print("X = impacto")
    print("O = disparo al agua")
    print("~ = agua sin disparar")
    print("- = casilla del rival a la que todavía no has disparado")
    print()
    print("Introduce primero la COLUMNA y después la FILA.")
    print("Ejemplo: 3 7 significa columna 3, fila 7.")
    print("Escribe 'salir' cuando sea tu turno para terminar la partida.")
    print("=" * 46)


def mostrar_tableros(jugador):
    print("\nTU TABLERO (barcos y disparos que has recibido)")
    jugador.mostrar_tablero()
    print("\nTUS DISPAROS CONTRA LA MÁQUINA")
    jugador.mostrar_disparos()
    print()


def pedir_coordenadas(tablero_rival):
    """Pide coordenadas y repite la pregunta si el dato no es válido."""
    while True:
        texto = input("Dispara (columna fila), o escribe 'salir': ").strip().lower()

        if texto == "salir":
            return None

        # Aceptamos, por ejemplo, tanto '3 7' como '3,7'.
        partes = texto.replace(",", " ").split()

        if len(partes) != 2:
            print("Introduce dos números: columna y fila. Ejemplo: 3 7.")
            continue

        if not partes[0].isdigit() or not partes[1].isdigit():
            print("Las coordenadas deben ser números enteros.")
            continue

        x = int(partes[0])
        y = int(partes[1])

        if x < 1 or x > TAMANO_TABLERO or y < 1 or y > TAMANO_TABLERO:
            print("Las coordenadas deben estar entre 1 y 10.")
            continue

        if tablero_rival.disparo_repetido(x, y):
            print("Ya has disparado a esa casilla. Prueba otra.")
            continue

        return x, y


def turno_jugador(jugador, maquina):
    """El jugador continúa disparando mientras acierte."""
    while maquina.vidas > 0:
        coordenadas = pedir_coordenadas(maquina)

        if coordenadas is None:
            return "salir"

        x, y = coordenadas
        resultado = maquina.disparar(x, y)
        jugador.registrar_disparo(x, y, resultado)

        if resultado == "hundido":
            print("¡HUNDIDO! Has destruido un barco completo.")
        elif resultado == "impacto":
            print("¡Impacto! Has acertado. Te toca otra vez.")
        else:
            print("Agua. Ahora juega la máquina.")
            return "fin"

    return "fin"


def turno_maquina(maquina, jugador):
    """La máquina dispara al azar y continúa mientras acierte."""
    while jugador.vidas > 0:
        x, y = maquina.obtener_disparo_aleatorio()
        resultado = jugador.disparar(x, y)
        maquina.registrar_disparo(x, y, resultado)

        print("La máquina dispara en columna {}, fila {}.".format(x, y))

        if resultado == "hundido":
            print("La máquina ha hundido uno de tus barcos.")
        elif resultado == "impacto":
            print("La máquina ha acertado y vuelve a disparar.")
        else:
            print("La máquina ha fallado. Vuelve a ser tu turno.")
            return
