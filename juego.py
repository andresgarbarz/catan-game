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

def construir(tablero, jugador, numero, clase):
	if clase is Asentamiento:
		tipo_pos = "vertice"
		chequeo = tablero.obtener_asentamiento
		accion = tablero.colocar_asentamiento
	else:
		tipo_pos = "arista"
		chequeo = tablero.obtener_camino
		accion = tablero.colocar_camino

	while True:
		s = input(f"Coloque {clase.__name__.lower()} n* {numero}: ")
		if (s == "fin"): return False
		vals = s.translate(str.maketrans('', '', string.punctuation)).split()
		if len(vals) != 2:
			print("Debe ingresar dos valores")
			continue
		ficha, pos = map(int, vals)
		
		if (ficha not in range(1,20)):
			print("Ficha fuera de rango, ingresa un número entre 1 y 19")
			continue
		if (pos not in range(1,7)):
			print(f"{tipo_pos.capitalize()} fuera de rango, ingresa un número entre 1 y 6")
			continue
		if chequeo(ficha, pos) is None:
			break
		print(f"Ya hay un {clase.__name__.lower()} en esa posición, intente de nuevo")
		
	accion(ficha, pos, clase(jugador))
	return True

def jugar_catan(jugadores,tablero):
	for i in range(2):
		orden = jugadores if i == 0 else reversed(jugadores)
		for j in orden:
			# Colocar asentamientos
			if not construir(tablero, j, i+1, Asentamiento, True): return

			# Colocar caminos
			if not construir(tablero, j, i+1, Camino, True): return

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
				if accion == "ase":
					construir(tablero, j, Asentamiento)
				elif accion == "fin":
					return
				elif accion == "pas":
					break