class Asentamiento:
    def __init__(self, jugador):
        self.jugador = jugador

class Ciudad:
    pass

class Camino:
    def __init__(self, jugador):
        self.jugador = jugador

class Jugador:
    """ players = []
    def __new__(cls, *args, **kwargs):
        p = super().__new__(cls, *args, **kwargs)
        Jugador.players.append(p.nombre) """
    #Esto fue un intento super complejo para obtener todos los jugadores porque nos olvidamos que era un parámetro de jugar_catan() y queríamos dejarlo porque no todos los días se sobreescriben métodos mágicos

    def __init__(self, nombre, color):
        self.nombre = nombre
        self.color = color
        self.recursos = {"Ladrillo": 0, "Piedra": 0, "Trigo": 0, "Lana": 0, "Madera": 0}
    def añadir_recurso(self, recurso):
        self.recursos[recurso] += 1
    def cantidad_de(self, recurso):
        return self.recursos[recurso]
    def cantidad_recursos(self):
        return self.recursos
    def quitar_recursos(self, recs):
        for r in recs:
            self.recursos[r] -= 1
            print("quitado")
            print(r)
    def players_in_game(players):
        return players