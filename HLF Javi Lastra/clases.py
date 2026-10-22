import random

from variables import (
    TAMANO_TABLERO,
    FLOTA,
    AGUA,
    BARCO,
    IMPACTO,
    AGUA_DISPARADA,
    SIN_DISPARAR,
)


class Tablero:
    def __init__(self, jugador):
        # Identifica al propietario de este tablero.
        self.jugador = jugador
        self.filas = TAMANO_TABLERO
        self.columnas = TAMANO_TABLERO

        # Este tablero contiene el agua, los barcos y los disparos recibidos.
        self.tablero = []
        for fila in range(self.filas):
            nueva_fila = []
            for columna in range(self.columnas):
                nueva_fila.append(AGUA)
            self.tablero.append(nueva_fila)

        # Este segundo tablero registra los disparos que hace este jugador.
        # No contiene los barcos del rival: solo impactos, agua o casillas pendientes.
        self.disparos = []
        for fila in range(self.filas):
            nueva_fila = []
            for columna in range(self.columnas):
                nueva_fila.append(SIN_DISPARAR)
            self.disparos.append(nueva_fila)

        # Guardamos las coordenadas de cada barco para detectar cuándo se hunde.
        self.barcos_colocados = []
        self.vidas = sum(FLOTA)

        # Cada jugador coloca su propia flota al crear el tablero.
        self.colocar_barcos()

    def colocar_barcos(self):
        """Coloca cada barco al azar, sin salirse del tablero ni solaparse."""
        for eslora in FLOTA:
            colocado = False

            while not colocado:
                orientacion = random.choice(["H", "V"])

                if orientacion == "H":
                    fila = random.randint(0, self.filas - 1)
                    columna = random.randint(0, self.columnas - eslora)
                    coordenadas = []
                    for paso in range(eslora):
                        coordenadas.append((fila, columna + paso))
                else:
                    fila = random.randint(0, self.filas - eslora)
                    columna = random.randint(0, self.columnas - 1)
                    coordenadas = []
                    for paso in range(eslora):
                        coordenadas.append((fila + paso, columna))

                # Solo colocamos el barco si todas sus casillas están vacías.
                libre = True
                for fila_barco, columna_barco in coordenadas:
                    if self.tablero[fila_barco][columna_barco] != AGUA:
                        libre = False

                if libre:
                    for fila_barco, columna_barco in coordenadas:
                        self.tablero[fila_barco][columna_barco] = BARCO
                    self.barcos_colocados.append(coordenadas)
                    colocado = True

    def disparar(self, x, y):
        """Recibe un disparo. x es la columna e y es la fila, ambas desde 1."""
        if x < 1 or x > self.columnas or y < 1 or y > self.filas:
            return "fuera"

        # Las listas empiezan en 0, pero las coordenadas que introduce el usuario en 1.
        fila = y - 1
        columna = x - 1
        casilla = self.tablero[fila][columna]

        if casilla == IMPACTO or casilla == AGUA_DISPARADA:
            return "repetido"

        if casilla == BARCO:
            self.tablero[fila][columna] = IMPACTO
            self.vidas = self.vidas - 1

            # Comprobamos si todas las casillas de ese barco han sido alcanzadas.
            for barco in self.barcos_colocados:
                if (fila, columna) in barco:
                    hundido = True
                    for fila_barco, columna_barco in barco:
                        if self.tablero[fila_barco][columna_barco] != IMPACTO:
                            hundido = False
                    if hundido:
                        return "hundido"
                    return "impacto"

            # Este punto no debería alcanzarse, pero mantenemos una respuesta clara.
            return "impacto"

        # Si no había barco, se marca la casilla como agua disparada.
        self.tablero[fila][columna] = AGUA_DISPARADA
        return "agua"

    def registrar_disparo(self, x, y, resultado):
        """Anota en el tablero de seguimiento un disparo hecho por este jugador."""
        fila = y - 1
        columna = x - 1

        if resultado == "agua":
            self.disparos[fila][columna] = AGUA_DISPARADA
        elif resultado == "impacto" or resultado == "hundido":
            self.disparos[fila][columna] = IMPACTO

    def disparo_repetido(self, x, y):
        """Indica si ya se ha disparado a esa casilla del tablero propio."""
        fila = y - 1
        columna = x - 1
        casilla = self.tablero[fila][columna]
        return casilla == IMPACTO or casilla == AGUA_DISPARADA

    def obtener_disparo_aleatorio(self):
        """Devuelve una coordenada aún no probada por el jugador que llama al método."""
        disponibles = []
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.disparos[fila][columna] == SIN_DISPARAR:
                    # Devolvemos (columna, fila), empezando ambas coordenadas en 1.
                    disponibles.append((columna + 1, fila + 1))

        return random.choice(disponibles)

    def mostrar_tablero(self):
        """Muestra los barcos propios y los disparos que se han recibido."""
        print("    ", end="")
        for columna in range(1, self.columnas + 1):
            print("{:2}".format(columna), end=" ")
        print()

        for fila in range(self.filas):
            print("{:2} |".format(fila + 1), end=" ")
            for columna in range(self.columnas):
                print("{:2}".format(self.tablero[fila][columna]), end=" ")
            print()

    def mostrar_disparos(self):
        """Muestra únicamente los disparos propios realizados contra el rival."""
        print("    ", end="")
        for columna in range(1, self.columnas + 1):
            print("{:2}".format(columna), end=" ")
        print()

        for fila in range(self.filas):
            print("{:2} |".format(fila + 1), end=" ")
            for columna in range(self.columnas):
                print("{:2}".format(self.disparos[fila][columna]), end=" ")
            print()
