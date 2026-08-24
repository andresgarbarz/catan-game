class Asentamiento:
	def __init__(self, jugador) -> None:
		self.jugador = jugador

	def dar_recurso(self, rec):
		self.jugador.añadir_recurso(rec)

class Ciudad:
	def __init__(self, jugador) -> None:
		self.jugador = jugador

class Camino:
	def __init__(self, jugador) -> None:
		self.jugador = jugador

class Jugador:
	def __init__(self, nombre, color) -> None:
		self.nombre = nombre
		self.color = color
		self.recursos = {rec: 0 for rec in ["Ladrillo", "Piedra", "Trigo", "Lana", "Madera"]}
		self.asentamientos = 0

	def añadir_recurso(self, rec):
		self.recursos[rec] += 1

	# TODO: Corregir esto y construir en juego.py
	def cobrar_asentamiento(self):
		materiales = {"Ladrillo": 1, "Madera": 1, "Lana": 1, "Trigo": 1}
		if all(self.recursos[rec] >= costo for rec, costo in materiales.items()):
			for rec, costo in materiales.items():
				self.recursos[rec] -= costo
		self.asentamientos += 1

	def cantidad_de(self, rec):
		return self.recursos[rec]

	def cant_asentamientos(self):
		return 