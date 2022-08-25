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
            num = randint(2, 12)
            pos = randint(1, 19) - 1
    print(n_used)

def jugar_catan(jugadores,tablero):
    pass