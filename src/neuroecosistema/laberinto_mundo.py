from collections import deque
from dataclasses import dataclass
import random
import heapq

DIRECCIONES = ((-1, 0), (1, 0), (0, -1), (0, 1))
NOMBRES = ('ARRIBA', 'ABAJO', 'IZQUIERDA', 'DERECHA')
MAPAS = (
    # Mapa 1: Selva abierta con claros extensos (15x15)
    (
        '###############',
        '#.............#',
        '#.###.###.###.#',
        '#.#.........#.#',
        '#.#.###.###.#.#',
        '#.....#.#.....#',
        '###.###.#.###.#',
        '#.....#...#...#',
        '#.###.###.###.#',
        '#.#.........#.#',
        '#.#.###.###.#.#',
        '#...#.....#...#',
        '#.###.###.###.#',
        '#.............#',
        '###############',
    ),
    # Mapa 2: Laberinto denso de enredaderas y espesura (15x15)
    (
        '###############',
        '#.#...#.#...#.#',
        '#.#.#.#.#.#.#.#',
        '#...#...#...#.#',
        '###.###.###.#.#',
        '#...#.......#.#',
        '#.#.#.###.#.#.#',
        '#.#...#.#...#.#',
        '#.#.#.#.#.#.#.#',
        '#.#...#...#...#',
        '###.###.###.###',
        '#.....#...#...#',
        '#.###.#.#.###.#',
        '#.............#',
        '###############',
    ),
    # Mapa 3: Sendero serpenteante del río (15x15)
    (
        '###############',
        '#.............#',
        '###.###.#.###.#',
        '#...#...#...#.#',
        '#.#.###.###.#.#',
        '#.#.........#.#',
        '#.###.###.###.#',
        '#...#...#...#.#',
        '#.#.###.###.#.#',
        '#.#.........#.#',
        '#.###.###.###.#',
        '#...#...#...#.#',
        '###.###.###.###',
        '#.............#',
        '###############',
    ),
)

def libres(mapa):
    return [(f, c) for f, fila in enumerate(mapa) for c, v in enumerate(fila) if v == '.']

def vecino(pos, accion):
    df, dc = DIRECCIONES[accion]
    return pos[0] + df, pos[1] + dc

def valido(mapa, pos):
    f, c = pos
    return 0 <= f < len(mapa) and 0 <= c < len(mapa[0]) and mapa[f][c] != '#'

def distancias_bfs(mapa, meta):
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    dist = {meta: 0}
    frontera = [(0, meta)]
    
    while frontera:
        _, actual = heapq.heappop(frontera)
        for a in range(4):
            siguiente = vecino(actual, a)
            if valido(mapa, siguiente):
                nueva_dist = dist[actual] + 1
                if siguiente not in dist or nueva_dist < dist[siguiente]:
                    dist[siguiente] = nueva_dist
                    f_score = nueva_dist + heuristica(siguiente, meta)
                    heapq.heappush(frontera, (f_score, siguiente))
    return dist

def accion_experta(mapa, origen, dist):
    if origen not in dist or dist[origen] == 0:
        return None
    opciones = [(dist.get(vecino(origen, a), 10**9), a) for a in range(4)]
    minimo, accion = min(opciones)
    assert minimo < dist[origen]
    return accion