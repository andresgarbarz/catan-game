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
                        ase = Asentamiento(jugador)
                        tablero.colocar_asentamiento(ficha, vertice, ase)
                        fichasnums[jugador].append(tablero.obtener_numero_de_ficha(ficha))
                        #Extra de recursos iniciales, puesto como documentación porque rompe los test (descomentar para probar)
                        """ if "segundo asentamiento" in message:
                            for f in range(19):
                                for j in range(6):
                                    settle = tablero.obtener_asentamiento(f+1, j+1)
                                    if settle == ase:
                                        settle.jugador.añadir_recurso(tablero.obtener_recurso_de_ficha(f+1)) """
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
    
    #Turnos normales
    playing = True
    n = 0
    while playing:
        try:
            turno_de = jugadores[n].nombre
        except:
            n = 0
            turno_de = jugadores[n].nombre
        print("Turno de "+turno_de)
        num = tirar_dados()
        for i in range(19):
            if tablero.obtener_numero_de_ficha(i+1) == num:
                for j in range(6):
                    settle = tablero.obtener_asentamiento(i+1, j+1)
                    if settle:
                        settle.jugador.añadir_recurso(tablero.obtener_recurso_de_ficha(i+1))
            miturno = True
            while miturno:
                cinput = input("Inserte un comando: ").strip()
                if "tra" in cinput:
                    command, p2, rd, cd, rr, cr = cinput.split()
                    cd, cr = int(cd), int(cr)
                else:
                    try:
                        command, val1, val2 = cinput.split()
                        val1, val2 = int(val1), int(val2)
                    except:
                        command = cinput
                if command == "fin":
                    playing = False
                    return
                elif command == "pas":
                    print("turno pasado")
                    miturno = False
                    n+=1
                elif command == "tra":
                    p2 = [p for p in jugadores if p2 == p.nombre.lower()][0]
                    for r in range(cd):
                        p2.añadir_recurso(rd)
                    rd = [rd*cd]
                    jugador.quitar_recursos(rd)

                    for r in range(cr):
                        jugador.añadir_recursos(rr)
                    rr = [rr*cr]
                    p2.quitar_recursos(rr)
                elif command == "ase":
                    mats = jugador.cantidad_recursos()
                    if mats["Ladrillo"] >= 1 and mats["Madera"] >= 1 and mats["Lana"] >= 1 and mats["Trigo"] >= 1:
                        jugador.quitar_recursos(["Ladrillo", "Madera", "Lana", "Trigo"])
                        tablero.colocar_asentamiento(val1, val2, Asentamiento(jugador))
                elif command == "cam":
                    mats = jugador.cantidad_recursos()
                    if mats["Ladrillo"] >= 1 and mats["Madera"] >= 1:
                        jugador.quitar_recursos(["Ladrillo", "Madera"])
                        tablero.colocar_camino(val1, val2, Camino(jugador))
                else:
                    pass