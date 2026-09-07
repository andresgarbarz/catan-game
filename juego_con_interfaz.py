import builtins
import os
import sys

# x, y from top-left of the display
os.environ["SDL_VIDEO_WINDOW_POS"] = "100,50"  

from clases import Jugador
from interfaz import jugar_con_interfaz
from juego import rellenar_tablero
from tablero import TableroCatan

andy = Jugador("Andy", (255,0,0))
natan = Jugador("Natan", (0,255,0))

# Lista de jugadores
jugadores = [andy, natan]

# Tablero
tablero_a_jugar = TableroCatan()

# No se olviden de rellenar el tablero!
rellenar_tablero(tablero_a_jugar)

if "start" in sys.argv[1:]:
    colocaciones = ["1 1", "1 1", "2 2", "2 2", "3 3", "3 3", "4 4", "4 4"]
    _input = builtins.input
    def input_start(prompt=""):
        if colocaciones:
            valor = colocaciones.pop(0)
            print(prompt + valor)
            return valor
        return _input(prompt)
    builtins.input = input_start

# Vamo a juga
jugar_con_interfaz(jugadores,tablero_a_jugar)