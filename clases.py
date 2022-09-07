class Asentamiento:
    def __init__(self, jugador):
        self.jugador = jugador

class Ciudad:
    pass

class Camino:
    def __init__(self, jugador):
        self.jugador = jugador

class Jugador:
    def __init__(self, nombre, color):
        self.nombre = nombre
        self.color = color
        self.recursos = {"Ladrillo": 0, "Piedra": 0, "Trigo": 0, "Lana": 0, "Madera": 0}
    def añadir_recurso(self, recurso):
        self.recursos[recurso] += 1
    def cantidad_de(self, recurso):
        return self.recursos[recurso]