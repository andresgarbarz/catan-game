import random
from re import M
import string

from _pytest._py.error import R
from numpy.char import isalpha, isdigit

from clases import Asentamiento, Camino
ORDEN_ESPECIAL = True

MATERIALES = ["Ladrillo", "Piedra", "Trigo", "Lana", "Madera"]

ERROR_INT_FORMAT = "Para intercambiar, ingrese 'int [target] quiero [cant] [recurso] (n veces) doy [cant] [recurso] (m veces)'"

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

def construir(tablero, jugador, tipo_construccion, coords, esGratis=False):
	if len(coords) != 2:
		print("Debe ingresar dos valores")
		return False
	ficha, pos = map(int, coords)
	return jugador.construir(tipo_construccion, tablero, ficha, pos, esGratis)

def int_calcular_costos(lista_recursos):
	if len(lista_recursos) % 2 != 0:
		print(ERROR_INT_FORMAT)
		return False

	costos = {}

	for i in range(0, len(lista_recursos), 2):
		cant = lista_recursos[i]
		rec = lista_recursos[i+1].capitalize()
		if not isdigit(cant) or not isalpha(rec):
			print(ERROR_INT_FORMAT)
			return False

		if rec not in MATERIALES:
			print("Debe ingresar un recurso válido, la lista es:", MATERIALES)
			return False

		cant = int(cant)
		if cant < 1:
			print("No es posible intercambiar 0 recursos, no se aceptan regalos!")
			return False

		costos[rec] = cant	
	return costos

def jugar_catan(jugadores,tablero):
	# Set up
	for i in range(2):
		orden = jugadores if i == 0 else reversed(jugadores)
		for j in orden:
			for tipo_construccion in (Asentamiento, Camino):
				# Intento construir
				while True:
					s = input(f"Coloque {tipo_construccion.__name__.lower()} n* {i+1}: ")
					if s == "fin":
						return
					coords = s.translate(str.maketrans('', '', string.punctuation)).split()
					construccion = construir(tablero, j, tipo_construccion, coords, esGratis=True)
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
				partes = accion.lower().translate(str.maketrans('', '', string.punctuation)).split()
				cmd = partes[0] if partes else ""
				if cmd == "ase":
					construir(tablero, j, Asentamiento, partes[1:])
				elif cmd == "cam":
					construir(tablero, j, Camino, partes[1:])
				elif cmd == "int":	
					# Formato inválido 
					if len(partes) < 8 or partes[2] != "quiero" or "doy" not in partes[:-2]:
						print(ERROR_INT_FORMAT)
						continue

					# Obtengo target
					nombres_otros = []
					target = None
					for jug in jugadores:
						if jug != j:
							nombres_otros.append(jug.nombre)
							if jug.nombre.lower() == partes[1]:
								target = jug

					# Jugador inválido
					if not target:
						print("Debe ingresar un nombre de jugador válido.\nLa lista de jugadores es:", nombres_otros)
						continue

					# Chequeo materiales deseados
					doy_pos = partes.index('doy')
					deseados = partes[3:doy_pos]
					recibidos = int_calcular_costos(deseados)
					if not recibidos:
						continue

					# Chequeo materiales ofrecidos
					ofrecidos = partes[doy_pos+1:]
					entregados = int_calcular_costos(ofrecidos)
					if not entregados:
						continue
					
					# Tradear
					j.cobrar(entregados)
					target.cobrar(recibidos)

					j.heredar(recibidos)
					target.heredar(entregados)

					# Formato de intercambio:
					# int [target-nombre] [{Recursos-deseados}] [{Recursos-ofrecidos}]
					# Ejemplo:
					# int Natan quiero 1 Lana 1 Trigo doy 1 Ladrillo
					
				elif cmd == "fin":
					return
				elif cmd == "pas":
					break