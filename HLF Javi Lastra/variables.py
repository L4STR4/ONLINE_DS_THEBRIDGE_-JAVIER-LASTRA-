
TAMANO_TABLERO = 10 # Constante del juego no cambia durante la partida.
 
# Cada número representa la eslora hay cuatro barcos de 1 casilla, tres de 2, dos de 3 y uno de 4. 
FLOTA = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
 
# Nombre de cada barco según su eslora
NOMBRES_BARCOS = {
    4: "Portaaviones",
    3: "Acorazado",
    2: "Destructor",
    1: "Patrullero",
}
 
# Símbolos que se utilizan al mostrar los tableros.

AGUA = "~"                 # Casilla de agua sin disparar
BARCO = "B"                # Parte de un barco que no ha recibido un impacto
IMPACTO = "X"              # Disparo que ha acertado
AGUA_DISPARADA = "O"       # Disparo que ha caído en el agua
SIN_DISPARAR = "-"         # Casilla a la que todavía no se ha disparado
 