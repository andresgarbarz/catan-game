# Camino mas largo
def largo(nodo, jugador, usadas):
    mejor = 0
    for arista in nodo.aristas:
        if arista is None or arista in usadas:
            continue
        camino = arista.contenido
        if camino is None or camino.jugador != jugador:
            continue
        otro = arista.nodos[0] if arista.nodos[1] is nodo else arista.nodos[1]
        usadas.add(arista)
        extra = 0
        if otro.contenido is None or otro.contenido.jugador == jugador:
            extra = largo(otro, jugador, usadas)
        mejor = max(mejor, 1 + extra)
        usadas.remove(arista)
    return mejor

def larguisimo(tablero, jugador):
    nodos = set()
    for f in range(1, 20):
        for v in range(1, 7):
            arista = tablero.obtener_arista(f, v)
            if arista.contenido is not None and arista.contenido.jugador == jugador:
                for nodo in arista.nodos:
                    if nodo is not None:
                        nodos.add(nodo)
    return max((largo(n, jugador, set()) for n in nodos), default=0)