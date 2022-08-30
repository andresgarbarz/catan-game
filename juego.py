from random import randint
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
    pass