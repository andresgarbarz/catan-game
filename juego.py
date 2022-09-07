from random import randint
from clases import Asentamiento, Camino


ORDEN_ESPECIAL = False

def tirar_dados():
    return randint(1, 6) + randint(1, 6)

def rellenar_tablero(tablero):
    once = [2, 12]
    twice = [3, 4, 5, 6, 8, 9, 10, 11]
    n_used = [None]*19
    n_used[9] = 7
    num = randint(2, 12)
    pos = randint(1, 19) - 1
    while None in n_used:
        if pos == 9:
            pos = randint(1, 19) - 1
        elif num == 7:
            num = randint(2, 12)
        elif num in once and num in n_used:
            num = randint(2, 12)
        elif num in twice and n_used.count(num) >= 2:
            num = randint(2, 12)
        else:
            n_used[pos] = num
            tablero.colocar_numero(pos+1, num)
            num = randint(2, 12)
            pos = randint(1, 19) - 1
    print(n_used)

    m_used = [None]*19
    materials = ["Ladrillo", "Piedra", "Trigo", "Lana", "Madera"]
    three = ["Ladrillo", "Piedra"]
    four = ["Trigo", "Lana", "Madera"]
    mat = materials[randint(1, 5) - 1]
    pos = randint(1, 19) - 1
    while None in m_used:
        if pos == 9:
           m_used[pos] = ""
           pos = randint(1, 19) - 1
        elif mat in three and m_used.count(mat) >= 3:
            mat = materials[randint(1, 5) - 1]
        elif mat in four and m_used.count(mat) >= 4:
            mat = materials[randint(1, 5) - 1]
        else:
            m_used[pos] = mat
            tablero.colocar_recurso(pos+1, mat)
            mat = materials[randint(1, 5) - 1]
            pos = randint(1, 19) - 1
    m_used[9] = None
    print(m_used)        

def jugar_catan(jugadores,tablero):
    fichasnums = {}
    for jugador in jugadores:
        fichasnums[jugador] = []
    for jugador in jugadores:
        for i in range(4):
            a_valid = False
            c_valid = False
            if i%2 == 0:
                if i == 0:
                    message = "Coloque primer asentamiento: "
                else:
                    message = "Coloque segundo asentamiento: "
                while not a_valid:
                    userinput = input(""+message).strip()
                    if userinput == "fin": return
                    ficha, vertice = userinput.split()
                    ficha, vertice = int(ficha), int(vertice)
                    if ficha in range(1, 20) and vertice in range(1, 7):
                        a_valid = True
                        tablero.colocar_asentamiento(ficha, vertice, Asentamiento(jugador))
                        fichasnums[jugador].append(tablero.obtener_numero_de_ficha(ficha))
            else:
                if i == 1:
                    message = "Coloque primer camino: "
                else:
                    message = "Coloque segundo camino: "
                while not c_valid:
                    userinput = input(""+message).strip()
                    if userinput == "fin": return
                    ficha, vertice = userinput.split()
                    ficha, vertice = int(ficha), int(vertice)
                    if ficha in range(1, 20) and vertice in range(1, 7):
                        c_valid = True
                        tablero.colocar_camino(ficha, vertice, Camino(jugador))
    for jugador in jugadores:
        num = tirar_dados()
        for i in range(19):
            if tablero.obtener_numero_de_ficha(i+1) == num:
                for j in range(6):
                    settle = tablero.obtener_asentamiento(i+1, j+1)
                    if settle:
                        settle.jugador.añadir_recurso(tablero.obtener_recurso_de_ficha(i+1))
        command = input("Inserte un comando: ")
        if command == "fin":
            return