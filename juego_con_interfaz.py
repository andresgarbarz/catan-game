from clases import Jugador
from interfaz import jugar_con_interfaz
from juego import rellenar_tablero, tirar_dados
from tablero import TableroCatan

andy = Jugador("Andy", (255,0,0))
natan = Jugador("Natan", (0,255,0))

# Lista de jugadores
jugadores = [andy, natan]

# Tablero
tablero_a_jugar = TableroCatan()

# No se olviden de rellenar el tablero!
rellenar_tablero(tablero_a_jugar)

# Vamo a juga
jugar_con_interfaz(jugadores,tablero_a_jugar)