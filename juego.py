import random
import string

from clases import Asentamiento, Camino
ORDEN_ESPECIAL = True

def tirar_dados():
	return random.randint(1,6) + random.randint(1,6)

def rellenar_tablero(tablero):
	recursos = (["Ladrillo"]*3 + ["Piedra"]*3 + ["Trigo"]*4 + ["Lana"]*4 + ["Madera"]*4)
	random.shuffle(recursos)

	# Orden de numeros de Catan original
	numeros = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]

	ESPIRALES = [
		[1, 4, 8, 13, 17, 18, 19, 16, 12, 7, 3, 2, 5, 9, 14, 15, 11, 6], # Esquina 1
		[8, 13, 17, 18, 19, 16, 12, 7, 3, 2, 1, 4, 9, 14, 15, 11, 6, 5], # Esquina 8
		[17, 18, 19, 16, 12, 7, 3, 2, 1, 4, 8, 13, 14, 15, 11, 6, 5, 9], # Esquina 17
		[19, 16, 12, 7, 3, 2, 1, 4, 8, 13, 17, 18, 15, 11, 6, 5, 9, 14], # Esquina 19
		[12, 7, 3, 2, 1, 4, 8, 13, 17, 18, 19, 16, 11, 6, 5, 9, 14, 15], # Esquina 12
		[3, 2, 1, 4, 8, 13, 17, 18, 19, 16, 12, 7, 6, 5, 9, 14, 15, 11], # Esquina 3
	]
	espiral = random.choice(ESPIRALES)

	j = 0
	for ficha in espiral:
		tablero.colocar_recurso_y_numero(ficha, recursos[j], numeros[j])
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
				# Intento construir
				while True:
					s = input(f"Coloque {clase.__name__.lower()} n* {i+1}: ")
					if s == "fin":
						return
					coords = s.translate(str.maketrans('', '', string.punctuation)).split()
					construccion = construir(tablero, j, clase, coords, esGratis=True)
					if construccion:
						break
				# Recursos iniciales
				if i == 1 and isinstance(construccion, Asentamiento):
					ficha, vertice = map(int, coords)
					nodo = tablero.obtener_nodo(ficha, vertice)
					for f in range(1, 20):
						for v in range(1, 7):
							if tablero.obtener_nodo(f, v) == nodo:
								construccion.dar_recurso(tablero.obtener_recurso_de_ficha(f))

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
					asentamientos = tablero.asentamientos_por_ficha(ficha)
					for ase in asentamientos:
						if ase is not None:
							ase.dar_recurso(tablero.obtener_recurso_de_ficha(ficha))
			# Acciones
			while True:
				accion = input(f"{j.nombre}, qué desea hacer: ")
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