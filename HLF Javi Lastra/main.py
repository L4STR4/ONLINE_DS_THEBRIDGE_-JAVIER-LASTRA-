
from clases import Tablero
from funciones import imprimir_bienvenida, mostrar_tableros, turno_jugador, turno_maquina


def main():
    imprimir_bienvenida()

    # Los tableros se crean una sola vez al inicio de la partida.
    jugador = Tablero("Jugador")
    maquina = Tablero("Máquina")

    print("Tu flota y la de la máquina se han colocado aleatoriamente.")
    input("Pulsa Intro para comenzar...")

    partida_abandonada = False

    while jugador.vidas > 0 and maquina.vidas > 0:
        mostrar_tableros(jugador)

        resultado = turno_jugador(jugador, maquina)
        if resultado == "salir":
            partida_abandonada = True
            break

        # Si el rival ya no tiene barcos, no debe jugar la máquina.
        if maquina.vidas == 0:
            break

        turno_maquina(maquina, jugador)

    print("\n" + "=" * 46)
    if partida_abandonada:
        print("Has salido de la partida. ¡Hasta la próxima!")
    elif maquina.vidas == 0:
        print("¡ZORIONAK! Has hundido toda la flota enemiga y has ganado.")
    else:
        print("La máquina ha hundido toda tu flota. Esta vez gana la máquina.")

    print("Barcos restantes del jugador: {} casillas.".format(jugador.vidas))
    print("Barcos restantes de la máquina: {} casillas.".format(maquina.vidas))
    print("=" * 46)

    # Al final se muestra el tablero de seguimiento para consultar la partida.
    print("\nTus disparos finales:")
    jugador.mostrar_disparos()
    print("\nTablero final de la máquina (solo para comprobar la partida):")
    maquina.mostrar_tablero()


if __name__ == "__main__":
    main()
