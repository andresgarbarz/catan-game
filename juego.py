import random
from re import M
import string
from typing import Any

from victoria import larguisimo 

from _pytest._py.error import R
from numpy.char import isalpha, isdigit

from clases import Asentamiento, Caballero, Camino, Caminos, Ciudad, Monopolio, Puntos, Recursos
ORDEN_ESPECIAL = True

MATERIALES = ["Ladrillo", "Piedra", "Trigo", "Lana", "Madera"]

ERROR = {
    "int": (
        "Para intercambiar, ingrese "
        "'int [target] quiero [cant] [recurso] (n veces) doy [cant] [recurso] (m veces)'"
    ),
    "desc": (
        "Ingresa "
        "'desc [cant] [recurso] (n veces) ... [cant] [recurso] (m veces)'"
    ),
}

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

def calcular_costos(lista_recursos, op):
	if len(lista_recursos) % 2 != 0:
		print(ERROR[op])
		return False

	costos = {}

	for i in range(0, len(lista_recursos), 2):
		cant = lista_recursos[i]
		rec = lista_recursos[i+1].capitalize()
		if not isdigit(cant) or not isalpha(rec):
			print(ERROR[op])
			return False

		if rec not in MATERIALES:
			print("Debe ingresar un recurso válido, la lista es:", MATERIALES)
			return False

		cant = int(cant)
		if cant < 1:
			print("No es posible dar 0 recursos")
			return False

		costos[rec] = cant	
	return costos

def usar_ladron(tablero, j, ficha_ladron):
	# Colocar ladron
	while True:
		ladron_target = input(f"{j.nombre}, a qué ficha desea mover el ladrón: ")
		if not isdigit(ladron_target):
			print(f"Debe ingresar un número entre 1 y 19, excepto el 10 y {ficha_ladron}")
			continue
		ladron_target = int(ladron_target)
		if ladron_target == 10 or ladron_target not in range(1,20) or tablero.tiene_ladron(ladron_target):
			str_10 = "y 10" if ficha_ladron != 10 else ""
			print(f"Debe ingresar un número entre 1 y 19, excepto {ficha_ladron} {str_10}")
			continue
		tablero.sacar_ladron(ficha_ladron)
		tablero.colocar_ladron(ladron_target)
		ficha_ladron = ladron_target
		break

	# Armo set de robables
	robables = set[Any]()
	for v in range(1, 7):
		ase = tablero.obtener_asentamiento(ficha_ladron, v)
		if ase and ase.jugador and ase.jugador != j:
			robables.add(ase.jugador)

	# Elegir victima
	while True:
		# No hay robables
		if not robables:
			print("No tenés a quien robarle, salamín!")
			break
		
		# Busco victima
		victima = None
		target = input("Ingrese el nombre de un jugador: ")

		nombres_robables = []
		for r in robables:
			nombres_robables.append(r.nombre)
			if target.lower() == r.nombre.lower():
				victima = r

		# Jugador inválido
		if not victima:
			print("Debe ingresar un nombre de jugador válido.\nLa lista de jugadores es:", list(nombres_robables))
			continue

		# Mezclar cartas
		cartas = [rec for rec, cant in victima.recursos.items() for i in range(cant)]
		random.shuffle(cartas)
		break

	# Robar
	while robables:
		if len(cartas) > 1:
			index = input(f"Ingrese un numero entre 1 y {len(cartas)}: ")
			if not isdigit(index) or int(index) not in range(1, len(cartas)+1):
				print(f"Tenes que ingresar un numero entre 1 y {len(cartas)+1}, capo!")
				continue

			index = int(index) - 1

			print(f"Robaste un {cartas[index]}")

		else:
			index = 0
			print(f"Robaste lo único que tenía {victima.nombre}: 1 {cartas[index]}")

		victima.cobrar({cartas[index]: 1})
		j.heredar({cartas[index]: 1})

		break

	return ficha_ladron

def jugar_catan(jugadores, tablero):
	camino_mas_largo = 4
	torre = None
	ejercito = 2
	general = None

	# mazo = ([Caballero]*14 + [Caminos]*2 + [Recursos]*2 + [Monopolio]*2 + [Puntos]*6)
	mazo = ([Caminos]*2)
	random.shuffle(mazo)

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

	ficha_ladron = 10
	# Juego
	while True:
		for j in jugadores:
			dados = tirar_dados()
			if dados == 7:
				# Descartar >7 cartas
				for jug in jugadores:
					total = sum(jug.recursos.values())
					if total > 7:
						while True:
							# desc 1 madera 3 lana
							accion = input(f"{jug.nombre} debe descartar {total//2} cartas, ingreselas con desc ... : ")
							indeseados = accion.lower().translate(str.maketrans('', '', string.punctuation)).split()

							if len(indeseados) < 3 or indeseados[0] != "desc":
								print(ERROR["desc"])
								continue

							descarte = calcular_costos(indeseados[1:], "desc")

							if not descarte:
								continue

							cant = sum(descarte.values())
							if cant != total // 2:
								print(f"Tenés que descartar {total//2} cartas, genio!")
								continue

							if not jug.cobrar(descarte):
								print(f"{jug.nombre}, no tenés esos recursos, ratón")
								continue
							
							break

				ficha_ladron = usar_ladron(tablero, j, ficha_ladron)

			for ficha in range(1, 20):
				# Desierto
				if ficha == 10:
					continue
				# Resto del tablero
				if (tablero.obtener_numero_de_ficha(ficha) == dados and not tablero.tiene_ladron(ficha)):
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

					# Recalculo camino más largo por si le cortaron a la torre
					if torre is not None:
						torre_long = larguisimo(tablero, torre)

					# Torre pierde camino más largo, veo si se lo doy a otro o no
					if torre is None or torre_long < camino_mas_largo:
						camino_mas_largo = 4
						longs = {}
						for juga in jugadores:
							l = larguisimo(tablero, juga)
							if l not in longs:
								longs[l] = []
							longs[l].append(juga)

						# Reviso que otros jugadores cumplan
						long_max = max(longs.keys())
						candidatos = []
						if long_max > camino_mas_largo:
							camino_mas_largo = long_max
							candidatos = longs[camino_mas_largo]

						if len(candidatos) == 1:
							torre = candidatos[0]
						elif torre in candidatos:
							continue
						else:
							torre = None
				elif cmd == "ciu":
					construir(tablero, j, Ciudad, partes[1:])
				elif cmd == "cam":
					construir(tablero, j, Camino, partes[1:])
					long = larguisimo(tablero, j)
					if long > camino_mas_largo:
						camino_mas_largo = long
						torre = j
						print(f"La torre ahora es {torre.nombre}")
				elif cmd == "int":	
					# Formato inválido 
					if len(partes) < 8 or partes[2] != "quiero" or "doy" not in partes[:-2]:
						print(ERROR[cmd])
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
					recibidos = calcular_costos(deseados, cmd)
					if not recibidos:
						continue

					# Chequeo materiales ofrecidos
					ofrecidos = partes[doy_pos+1:]
					entregados = calcular_costos(ofrecidos, cmd)
					if not entregados:
						continue
					
					# Tradear
					if not j.cobrar(entregados):
						print(f"{j.nombre}, no tenés esos recursos, ratón")
						continue

					if not target.cobrar(recibidos):
						print(f"{target.nombre} no tiene esos recursos, bobo")
						continue

					j.heredar(recibidos)
					target.heredar(entregados)

					# Formato de intercambio:
					# int [target-nombre] [{Recursos-deseados}] [{Recursos-ofrecidos}]
					# Ejemplo:
					# int Natan quiero 1 Lana 1 Trigo doy 1 Ladrillo
				elif cmd == "des":
					mazo = j.comprar_desarrollo(mazo)
				elif cmd == "cab":
					if Caballero.usar(j):
						usar_ladron(tablero, j, ficha_ladron)
					if j.caballeros > ejercito:
						ejercito += 1
						general = j
				elif cmd == "via":
					if Caminos.usar(j):
						for i in range(2):
							while True:
								s = input(f"Coloque el camino n* {i+1}: ")
								coords = s.translate(str.maketrans('', '', string.punctuation)).split()
								construccion = construir(tablero, j, tipo_construccion, coords, esGratis=True)
								if construccion:
									break
				elif cmd == "fin":
					return
				elif cmd == "pas":
					break