from interfaz import jugar_con_interfaz
from tablero import TableroCatan
from juego import rellenar_tablero

#Lista de jugadores
jugadores = []
#Tablero
tablero_a_jugar = TableroCatan()
rellenar_tablero(tablero_a_jugar)
#No se olviden de rellenar el tablero!
jugar_con_interfaz(jugadores,tablero_a_jugar)