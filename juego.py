import random
import string

from clases import Asentamiento, Camino
ORDEN_ESPECIAL = True

def tirar_dados():
	return random.randint(1,6) + random.randint(1,6)

def rellenar_tablero(tablero):
	recursos = (["Ladrillo"]*3 + ["Piedra"]*3 + ["Trigo"]*4 + ["Lana"]*4 + ["Madera"]*4)
	random.shuffle(recursos)
	
	numeros = [2, 12] + [x for x in range(3, 12) if x != 7]*2
	random.shuffle(numeros)

	j = 0
	for i in range(19):
		if i+1 == 10:
			continue
		tablero.colocar_recurso_y_numero(i+1, recursos[j], numeros[j])
		j += 1

def construir(tablero, jugador, clase, coords, esGratis=False):
	if len(coords) != 2:
		print("Debe ingresar dos valores")
		return False
	ficha, pos = map(int, coords)
	return jugador.construir(clase, tablero, ficha, pos, esGratis)

def jugar_catan(jugadores,tablero):

	# Set up
	for i in range(2):
		orden = jugadores if i == 0 else reversed(jugadores)
		for j in orden:
			for clase in (Asentamiento, Camino):
				while True:
					s = input(f"Coloque {clase.__name__.lower()} n* {i+1}: ")
					if s == "fin":
						return
					coords = s.translate(str.maketrans('', '', string.punctuation)).split()
					if construir(tablero, j, clase, coords, esGratis=True):
						break

	# Juego
	while True:
		for j in jugadores:
			dados = tirar_dados()
			for ficha in range(1, 20):
				# Desierto
				if ficha == 10:
					continue
				# Resto del tablero
				if (tablero.obtener_numero_de_ficha(ficha) == dados):
					for vertice in range(1, 7):
						ase = tablero.obtener_asentamiento(ficha, vertice)
						if ase is not None:
							ase.dar_recurso(tablero.obtener_recurso_de_ficha(ficha))
			# Acciones
			while True:
				accion = input("Que desea hacer: ")
				partes = accion.split()
				cmd = partes[0] if partes else ""
				if cmd == "ase":
					construir(tablero, j, Asentamiento, partes[1:])
				elif cmd == "cam":
					construir(tablero, j, Camino, partes[1:])
				elif cmd == "fin":
					return
				elif cmd == "pas":
					break