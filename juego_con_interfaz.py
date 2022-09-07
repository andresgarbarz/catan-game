from interfaz import jugar_con_interfaz
from tablero import TableroCatan
from juego import rellenar_tablero
from clases import Jugador

natan = Jugador("Natan", (0,255,0))
andy = Jugador("Andy", (255,0,0))
#Lista de jugadores
jugadores = [andy, natan]
#Tablero
tablero_a_jugar = TableroCatan()
rellenar_tablero(tablero_a_jugar)
#No se olviden de rellenar el tablero!
jugar_con_interfaz(jugadores,tablero_a_jugar)