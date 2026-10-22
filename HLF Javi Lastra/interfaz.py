# interfaz.py
# Version grafica de Hundir la flota.
# Este archivo utiliza la clase Tablero del programa original.
# No es necesario modificar main.py, clases.py, funciones.py ni variables.py.

from pathlib import Path
import tkinter as tk
from tkinter import messagebox

from clases import Tablero
from variables import (
    TAMANO_TABLERO,
    AGUA,
    BARCO,
    IMPACTO,
    AGUA_DISPARADA,
    SIN_DISPARAR,
    NOMBRES_BARCOS,
)


# Colores de la interfaz.
FONDO = "#edf4f8"
AZUL_OSCURO = "#17324d"
AZUL_MAR = "#dcecf5"
AZUL_BOTON = "#214d70"
VERDE_BARCO = "#b9ddc5"
ROJO_IMPACTO = "#d95757"
AGUA_DISPARADA_COLOR = "#9ed2e5"
TEXTO = "#1d3446"
BLANCO = "#ffffff"

# Alto (en pixeles) al que se reduce la imagen de la cabecera.
# Cambialo si la quieres mas grande o mas pequena.
ALTURA_CABECERA = 120


class JuegoGrafico:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Hundir la flota")
        self.ventana.geometry("1100x780")
        self.ventana.minsize(940, 700)
        self.ventana.configure(bg=FONDO)

        self.jugador = None
        self.maquina = None
        self.turno_jugador = True
        self.fin_partida = False
        self.after_maquina_id = None
        self.botones_enemigos = []
        self.casillas_jugador = []
        self.imagen_cabecera = None

        self.crear_interfaz()
        self.nueva_partida()

    def cargar_cabecera(self):
        """Carga cabecera.png reducida a ALTURA_CABECERA pixeles de alto.

        Devuelve None si no encuentra la imagen.
        """
        ruta_imagen = Path(__file__).with_name("cabecera.png")
        if not ruta_imagen.exists():
            return None

        try:
            # Con Pillow (si esta instalado) la imagen se ve mas nitida.
            from PIL import Image, ImageTk

            imagen = Image.open(ruta_imagen)
            ancho = round(imagen.width * ALTURA_CABECERA / imagen.height)
            imagen = imagen.resize((ancho, ALTURA_CABECERA), Image.LANCZOS)
            return ImageTk.PhotoImage(imagen)
        except ImportError:
            # Sin Pillow, tkinter solo puede reducir la imagen a la mitad,
            # a un tercio, etc. (numeros enteros).
            imagen = tk.PhotoImage(file=str(ruta_imagen))
            factor = max(1, round(imagen.height() / ALTURA_CABECERA))
            return imagen.subsample(factor, factor)

    def crear_interfaz(self):
        """Crea los titulos, los tableros, la leyenda y los botones."""
        cabecera = tk.Frame(self.ventana, bg=AZUL_OSCURO, padx=18, pady=6)
        cabecera.pack(fill="x")

        # La imagen se guarda en self para que tkinter no la borre.
        self.imagen_cabecera = self.cargar_cabecera()
        if self.imagen_cabecera is not None:
            tk.Label(
                cabecera,
                image=self.imagen_cabecera,
                bg=AZUL_OSCURO,
                borderwidth=0,
            ).pack()

        tk.Label(
            cabecera,
            text="Haz clic en una casilla del tablero enemigo para disparar",
            font=("Arial", 11),
            bg=AZUL_OSCURO,
            fg="#dceaf5",
        ).pack(pady=(2, 0))

        self.etiqueta_estado = tk.Label(
            self.ventana,
            text="Preparando la partida...",
            font=("Arial", 12, "bold"),
            bg=FONDO,
            fg=TEXTO,
            pady=12,
        )
        self.etiqueta_estado.pack(fill="x")

        marcadores = tk.Frame(self.ventana, bg=FONDO)
        marcadores.pack(fill="x", padx=20, pady=(0, 8))

        self.etiqueta_vidas_jugador = tk.Label(
            marcadores,
            text="Tu flota: 20 casillas",
            font=("Arial", 10, "bold"),
            bg=FONDO,
            fg=TEXTO,
        )
        self.etiqueta_vidas_jugador.pack(side="left", expand=True)

        self.etiqueta_vidas_maquina = tk.Label(
            marcadores,
            text="Flota enemiga: 20 casillas",
            font=("Arial", 10, "bold"),
            bg=FONDO,
            fg=TEXTO,
        )
        self.etiqueta_vidas_maquina.pack(side="right", expand=True)

        zona_tableros = tk.Frame(self.ventana, bg=FONDO)
        zona_tableros.pack(expand=True, fill="both", padx=12, pady=4)

        panel_propio = tk.LabelFrame(
            zona_tableros,
            text="TU TABLERO",
            font=("Arial", 11, "bold"),
            bg=FONDO,
            fg=TEXTO,
            padx=8,
            pady=8,
            labelanchor="n",
        )
        # anchor="n" pega los dos paneles arriba, para que queden alineados.
        panel_propio.pack(side="left", expand=True, padx=8, pady=4, anchor="n")

        panel_enemigo = tk.LabelFrame(
            zona_tableros,
            text="TABLERO ENEMIGO",
            font=("Arial", 11, "bold"),
            bg=FONDO,
            fg=TEXTO,
            padx=8,
            pady=8,
            labelanchor="n",
        )
        panel_enemigo.pack(side="left", expand=True, padx=8, pady=4, anchor="n")

        self.crear_tablero_propio(panel_propio)
        self.crear_tablero_enemigo(panel_enemigo)

        leyenda = tk.Frame(self.ventana, bg=FONDO, padx=10, pady=7)
        leyenda.pack(fill="x")

        tk.Label(
            leyenda,
            text="LEYENDA",
            font=("Arial", 9, "bold"),
            bg=FONDO,
            fg=TEXTO,
        ).pack(side="left", padx=(0, 10))

        self.elemento_leyenda(leyenda, "B", VERDE_BARCO, "Barco")
        self.elemento_leyenda(leyenda, "X", ROJO_IMPACTO, "Impacto")
        self.elemento_leyenda(leyenda, "O", AGUA_DISPARADA_COLOR, "Agua")
        self.elemento_leyenda(leyenda, "~", AZUL_MAR, "Agua sin disparar")
        self.elemento_leyenda(leyenda, "·", AZUL_BOTON, "Casilla enemiga sin probar", texto_claro=True)

        botones = tk.Frame(self.ventana, bg=FONDO, pady=7)
        botones.pack(fill="x")

        tk.Button(
            botones,
            text="Nueva partida",
            command=self.nueva_partida,
            font=("Arial", 10, "bold"),
            bg=AZUL_BOTON,
            fg=BLANCO,
            activebackground=AZUL_OSCURO,
            activeforeground=BLANCO,
            relief="flat",
            padx=14,
            pady=7,
            cursor="hand2",
        ).pack(side="left", padx=(25, 8))

        tk.Button(
            botones,
            text="Salir",
            command=self.ventana.destroy,
            font=("Arial", 10),
            bg="#dce3e8",
            fg=TEXTO,
            activebackground="#c4d0d8",
            relief="flat",
            padx=14,
            pady=7,
            cursor="hand2",
        ).pack(side="right", padx=(8, 25))

        tk.Label(
            self.ventana,
            text="Coordenadas: los números de arriba son las columnas y los de la izquierda son las filas.",
            font=("Arial", 9),
            bg=FONDO,
            fg="#546b7a",
            pady=7,
        ).pack(fill="x")

    def elemento_leyenda(self, marco, simbolo, color, texto, texto_claro=False):
        """Añade un simbolo y su descripcion a la leyenda."""
        caja = tk.Frame(marco, bg=FONDO)
        caja.pack(side="left", padx=5)
        tk.Label(
            caja,
            text=simbolo,
            width=2,
            font=("Arial", 9, "bold"),
            bg=color,
            fg=BLANCO if texto_claro else TEXTO,
            relief="flat",
        ).pack(side="left", padx=(0, 4))
        tk.Label(
            caja,
            text=texto,
            font=("Arial", 8),
            bg=FONDO,
            fg=TEXTO,
        ).pack(side="left")

    def crear_tablero_propio(self, marco):
        """Crea el tablero que muestra nuestros barcos y disparos recibidos."""
        self.casillas_jugador = []

        tk.Label(marco, text="F/C", bg=FONDO, fg=TEXTO, font=("Arial", 8, "bold")).grid(
            row=0, column=0, padx=1, pady=1
        )

        for columna in range(TAMANO_TABLERO):
            tk.Label(
                marco,
                text=str(columna + 1),
                width=3,
                bg=FONDO,
                fg=TEXTO,
                font=("Arial", 8, "bold"),
            ).grid(row=0, column=columna + 1, padx=1, pady=1)

        for fila in range(TAMANO_TABLERO):
            tk.Label(
                marco,
                text=str(fila + 1),
                width=2,
                bg=FONDO,
                fg=TEXTO,
                font=("Arial", 8, "bold"),
            ).grid(row=fila + 1, column=0, padx=1, pady=1)

            fila_casillas = []
            for columna in range(TAMANO_TABLERO):
                casilla = tk.Label(
                    marco,
                    text="~",
                    width=3,
                    height=1,
                    font=("Consolas", 11, "bold"),
                    bg=AZUL_MAR,
                    fg=TEXTO,
                    relief="flat",
                    padx=0,
                    pady=4,
                )
                casilla.grid(row=fila + 1, column=columna + 1, padx=1, pady=1)
                fila_casillas.append(casilla)
            self.casillas_jugador.append(fila_casillas)

    def crear_tablero_enemigo(self, marco):
        """Crea las casillas del tablero enemigo, que se pulsan para disparar.

        Usamos Label (igual que en el tablero propio) y no Button, porque un
        Button es siempre unos pixeles mas alto y los dos tableros no quedaban
        iguales. El clic se detecta con bind().
        """
        self.botones_enemigos = []

        tk.Label(marco, text="F/C", bg=FONDO, fg=TEXTO, font=("Arial", 8, "bold")).grid(
            row=0, column=0, padx=1, pady=1
        )

        for columna in range(TAMANO_TABLERO):
            tk.Label(
                marco,
                text=str(columna + 1),
                width=3,
                bg=FONDO,
                fg=TEXTO,
                font=("Arial", 8, "bold"),
            ).grid(row=0, column=columna + 1, padx=1, pady=1)

        for fila in range(TAMANO_TABLERO):
            tk.Label(
                marco,
                text=str(fila + 1),
                width=2,
                bg=FONDO,
                fg=TEXTO,
                font=("Arial", 8, "bold"),
            ).grid(row=fila + 1, column=0, padx=1, pady=1)

            fila_botones = []
            for columna in range(TAMANO_TABLERO):
                boton = tk.Label(
                    marco,
                    text="·",
                    width=3,
                    height=1,
                    font=("Consolas", 11, "bold"),
                    bg=AZUL_BOTON,
                    fg=BLANCO,
                    relief="flat",
                    padx=0,
                    pady=4,
                    cursor="hand2",
                )
                # Al hacer clic izquierdo en la casilla se dispara a (columna, fila).
                boton.bind(
                    "<Button-1>",
                    lambda evento, f=fila, c=columna: self.disparar_jugador(c + 1, f + 1),
                )
                boton.grid(row=fila + 1, column=columna + 1, padx=1, pady=1)
                fila_botones.append(boton)
            self.botones_enemigos.append(fila_botones)

    def nueva_partida(self):
        """Crea nuevos tableros y reinicia la partida sin cerrar la ventana."""
        # Cancela un disparo pendiente si se pulsa Nueva partida durante el turno
        # de la maquina, para que no afecte accidentalmente a la nueva partida.
        if self.after_maquina_id is not None:
            try:
                self.ventana.after_cancel(self.after_maquina_id)
            except tk.TclError:
                pass
            self.after_maquina_id = None

        self.jugador = Tablero("Jugador")
        self.maquina = Tablero("Máquina")
        self.turno_jugador = True
        self.fin_partida = False
        self.actualizar_tableros()
        self.mostrar_estado("Tu turno: elige una casilla del tablero enemigo.")

    def buscar_nombre_barco(self, tablero, x, y):
        """Devuelve el nombre del barco de `tablero` que ocupa la casilla (x, y).

        tablero.barcos_colocados guarda las coordenadas (fila, columna) de cada
        barco, empezando en 0. Por eso restamos 1 a x e y. El tamaño del barco
        es el numero de coordenadas que tiene, y con eso buscamos su nombre.
        """
        for barco in tablero.barcos_colocados:
            if (y - 1, x - 1) in barco:
                return NOMBRES_BARCOS[len(barco)]
        return "barco"

    def disparar_jugador(self, x, y):
        """Gestiona un disparo realizado al pulsar el tablero enemigo."""
        if self.fin_partida or not self.turno_jugador:
            return

        if self.jugador.disparos[y - 1][x - 1] != SIN_DISPARAR:
            return

        resultado = self.maquina.disparar(x, y)
        self.jugador.registrar_disparo(x, y, resultado)
        self.actualizar_tableros()

        if resultado == "fuera" or resultado == "repetido":
            self.mostrar_estado("Esa casilla no se puede utilizar. Elige otra.")
            return

        # Si el disparo ha hundido un barco, averiguamos cual era.
        nombre_barco = None
        if resultado == "hundido":
            nombre_barco = self.buscar_nombre_barco(self.maquina, x, y)

        if self.maquina.vidas == 0:
            self.fin_partida = True
            self.turno_jugador = False
            self.actualizar_tableros()
            self.mostrar_estado("HAS DEJADO EL TABLERO LISO.")
            messagebox.showinfo("Partida terminada",
                                "Has hundido el {}, el último barco enemigo.\n¡Zorionak! Eres un máquina.".format(nombre_barco)
                                )
            return

        if resultado == "hundido":
            self.mostrar_estado("¡HUNDIDO! Has hundido el {}.".format(nombre_barco))
            messagebox.showinfo(" OSO ONDO!",
                                 "Has hundido el {}. Sigue así.".format(nombre_barco)
                                 )
        elif resultado == "impacto":
            self.mostrar_estado("¡BAAA BUUUMMMM. Dale de nuevo.")
        else:
            self.turno_jugador = False
            self.actualizar_tableros()
            self.mostrar_estado("Fallaste. Ahora le toca a la máquina...")
            self.after_maquina_id = self.ventana.after(450, self.disparar_maquina)

    def disparar_maquina(self):
        """La máquina hace un disparo; si acierta, vuelve a disparar."""
        self.after_maquina_id = None
        if self.fin_partida:
            return

        x, y = self.maquina.obtener_disparo_aleatorio()
        resultado = self.jugador.disparar(x, y)
        self.maquina.registrar_disparo(x, y, resultado)
        self.actualizar_tableros()

        # Si el disparo ha hundido un barco tuyo, averiguamos cual era.
        nombre_barco = None
        if resultado == "hundido":
            nombre_barco = self.buscar_nombre_barco(self.jugador, x, y)

        if self.jugador.vidas == 0:
            self.fin_partida = True
            self.turno_jugador = False
            self.actualizar_tableros()
            self.mostrar_estado("El enemigo ha hundido tu flota. No queda ni el tato.")
            messagebox.showinfo("GAME OVER LOSER", 
                                "Te han hundido el {}, tu último barco.\nEres un pakete!".format(nombre_barco)
                                )
            return

        if resultado == "hundido":
            self.mostrar_estado(
                "Uy uy uy La máquina ha hundido tu {} (columna {}, fila {}). Vuelve a disparar.".format(nombre_barco, x, y)
            )
            self.after_maquina_id = self.ventana.after(450, self.disparar_maquina)
        elif resultado == "impacto":
            self.mostrar_estado(
                "La máquina ha acertado en columna {}, fila {}. Dispara otra vez.".format(x, y)
            )
            self.after_maquina_id = self.ventana.after(450, self.disparar_maquina)
        else:
            self.turno_jugador = True
            self.actualizar_tableros()
            self.mostrar_estado(
                "La máquina ha fallado en columna {}, fila {}. Tu turno: elige una casilla.".format(x, y)
            )

    def actualizar_tableros(self):
        """Dibuja el estado actual de ambos tableros en la ventana."""
        puede_disparar = self.turno_jugador and not self.fin_partida

        for fila in range(TAMANO_TABLERO):
            for columna in range(TAMANO_TABLERO):
                simbolo = self.jugador.tablero[fila][columna]
                texto, color_fondo, color_texto = self.estilo_casilla(simbolo, tablero_propio=True)
                self.casillas_jugador[fila][columna].configure(
                    text=texto,
                    bg=color_fondo,
                    fg=color_texto,
                )

                disparo = self.jugador.disparos[fila][columna]
                boton = self.botones_enemigos[fila][columna]
                if disparo == SIN_DISPARAR:
                    # La mano solo aparece cuando de verdad se puede disparar.
                    boton.configure(
                        text="·",
                        bg=AZUL_BOTON,
                        fg=BLANCO,
                        cursor="hand2" if puede_disparar else "arrow",
                    )
                else:
                    texto, color_fondo, color_texto = self.estilo_casilla(disparo, tablero_propio=False)
                    boton.configure(
                        text=texto,
                        bg=color_fondo,
                        fg=color_texto,
                        cursor="arrow",
                    )

        self.etiqueta_vidas_jugador.configure(
            text="Tu flota: {} casillas".format(self.jugador.vidas)
        )
        self.etiqueta_vidas_maquina.configure(
            text="Flota enemiga: {} casillas".format(self.maquina.vidas)
        )

    def estilo_casilla(self, simbolo, tablero_propio):
        """Devuelve el texto y los colores adecuados para un simbolo."""
        if simbolo == BARCO and tablero_propio:
            return "B", VERDE_BARCO, "#214d35"
        if simbolo == IMPACTO:
            return "X", ROJO_IMPACTO, BLANCO
        if simbolo == AGUA_DISPARADA:
            return "O", AGUA_DISPARADA_COLOR, "#17445a"
        if simbolo == AGUA and tablero_propio:
            return "~", AZUL_MAR, "#537d94"
        return "·", AZUL_BOTON, BLANCO

    def mostrar_estado(self, mensaje):
        self.etiqueta_estado.configure(text=mensaje)


def main():
    ventana = tk.Tk()
    JuegoGrafico(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
