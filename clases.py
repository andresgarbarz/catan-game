class Construccion:
	tipo_pos = "posición"
	costo = {}

	def __init__(self, jugador) -> None:
		self.jugador = jugador

	@classmethod
	def posicion_valida(cls, tablero, ficha, pos, jugador):
		if ficha not in range(1, 20):
			print("Ficha fuera de rango, ingresa un número entre 1 y 19")
			return False
		if pos not in range(1, 7):
			print(f"{cls.tipo_pos.capitalize()} fuera de rango, ingresa un número entre 1 y 6")
			return False
		if not cls.construccion_valida(tablero, ficha, pos, jugador):
			print("No podes construir en esa posición, intenta de nuevo")
			return False
		if cls.ocupado(tablero, ficha, pos):
			print(f"Ya hay un {cls.__name__.lower()} en esa posición, intente de nuevo")
			return False
		return True

	@classmethod
	def construccion_valida(cls, tablero, ficha, pos, jugador):
		raise NotImplementedError

	@classmethod
	def ocupado(cls, tablero, ficha, pos):
		raise NotImplementedError

	@classmethod
	def colocar_en(cls, tablero, ficha, pos, jugador):
		raise NotImplementedError

class Asentamiento(Construccion):
	tipo_pos = "vertice"
	costo = {"Ladrillo": 1, "Madera": 1, "Lana": 1, "Trigo": 1}

	def dar_recurso(self, rec):
		self.jugador.añadir_recurso(rec)

	@classmethod
	def ocupado(cls, tablero, ficha, pos):
		return tablero.obtener_asentamiento(ficha, pos) is not None

	@classmethod
	def construccion_valida(cls, tablero, ficha, pos, jugador):
		if jugador.caminos < 2:
			camsCheck = True
		else:
			cams = tablero.caminos_adyacentes_a_nodo(ficha, pos)
			camsCheck = cams and any([cam.jugador == jugador for cam in cams])
		return not tablero.asentamientos_adyacentes_a_nodo(ficha, pos) and camsCheck

	@classmethod
	def colocar_en(cls, tablero, ficha, pos, jugador):
		jugador.puntos += 1
		return tablero.colocar_asentamiento(ficha, pos, cls(jugador))

class Ciudad(Construccion):
	tipo_pos = "vertice"
	costo = {"Trigo": 2, "Piedra": 3}

	def dar_recurso(self, rec):
		for _ in range(2):
			self.jugador.añadir_recurso(rec)

	@classmethod
	def ocupado(cls, tablero, ficha, pos):
		return isinstance(tablero.obtener_asentamiento(ficha, pos), Ciudad)

	@classmethod
	def colocar_en(cls, tablero, ficha, pos, jugador):
		jugador.puntos += 1
		tablero.colocar_asentamiento(ficha, pos, cls(jugador))

	@classmethod
	def construccion_valida(cls, tablero, ficha, pos, jugador):
		ase = tablero.obtener_asentamiento(ficha, pos)
		return ase is not None and ase.jugador == jugador

class Camino(Construccion):
	tipo_pos = "arista"
	costo = {"Ladrillo": 1, "Madera": 1}

	@classmethod
	def ocupado(cls, tablero, ficha, pos):
		return tablero.obtener_camino(ficha, pos) is not None

	@classmethod
	def construccion_valida(cls, tablero, ficha, pos, jugador):
		arista = tablero.obtener_arista(ficha, pos)
		if arista.contenido:
			return False
		for nodo in arista.nodos:
			if nodo is None:
				continue
			if nodo.contenido and nodo.contenido.jugador == jugador:
				return True
			cams = [a.contenido for a in nodo.aristas if a is not None and a.contenido is not None]
			if any(cam.jugador == jugador for cam in cams) and not nodo.contenido:
				return True
		return False

	@classmethod
	def colocar_en(cls, tablero, ficha, pos, jugador):
		jugador.caminos += 1
		return tablero.colocar_camino(ficha, pos, cls(jugador))

class CartaDesarrollo:
	costo = {"Piedra": 1, "Trigo": 1, "Lana": 1}
	usable = False
	mensaje_falta = "No tiene esa carta."

	@classmethod
	def usar(cls, jugador):
		if cls not in jugador.cartas:
			print(cls.mensaje_falta)
			return False
		jugador.cartas.remove(cls)
		return True

class Caballero(CartaDesarrollo):
	mensaje_falta = "No tiene un caballero, don."

	@classmethod
	def usar(cls, jugador):
		if not super().usar(jugador):
			return False
		jugador.caballeros += 1
		return True

class Caminos(CartaDesarrollo):
	mensaje_falta = "No tiene carta de caminos, mister."

class Recursos(CartaDesarrollo):
	mensaje_falta = "No tenés carta de recursos, compañero"

class Monopolio(CartaDesarrollo):
	mensaje_falta = "No tiene carta de monopolio, socio"

class Puntos(CartaDesarrollo):
	@classmethod
	def usar(cls, jugador):
		raise NotImplementedError

class Jugador:
	def __init__(self, nombre, color) -> None:
		self.nombre = nombre
		self.color = color
		self.recursos = {rec: 0 for rec in ["Ladrillo", "Piedra", "Trigo", "Lana", "Madera"]}
		# TODO: Chequear
		self.caminos = 0
		self.puntos = 0
		
		self.caballeros = 0
		# Cartas de desarrollo, salvo puntos
		self.cartas = []

	def añadir_recurso(self, rec):
		self.recursos[rec] += 1

	def puede_pagar(self, costo):
		return all(self.recursos[rec] >= n for rec, n in costo.items())

	def cobrar(self, costo):
		if not self.puede_pagar(costo):
			return False
		for rec, n in costo.items():
			self.recursos[rec] -= n
		return True

	def heredar(self, costo):
		for rec, n in costo.items():
			self.recursos[rec] += n

	def construir(self, clase, tablero, ficha, pos, gratis=False):
		if not clase.posicion_valida(tablero, ficha, pos, self):
			return False
		if not gratis and not self.cobrar(clase.costo):
			print("No tiene recursos suficientes")
			return False
		return clase.colocar_en(tablero, ficha, pos, self)

	def comprar_desarrollo(self, mazo):
		if not self.cobrar(CartaDesarrollo.costo):
			print("No tiene recursos suficientes")
			return False
		if len(mazo) == 0:
			print("No hay más cartas de desarrollo en el mazo")
			return False
		carta = mazo.pop()
		print(f"{self.nombre} obtuvo {carta}")
		self.cartas.append(carta)
		if carta == Puntos:
			self.puntos += 1
		return mazo

	def cantidad_de(self, rec):
		return self.recursos[rec]