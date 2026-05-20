from collections import deque

# Representación del estado resuelto del cubo 3x3x3
ESTADO_RESUELTO = (
    'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W',  # 0-8: Arriba (U)
    'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',  # 9-17: Izquierda (L)
    'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R',  # 18-26: Frente (F)
    'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B',  # 27-35: Derecha (R)
    'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',  # 36-44: Atrás (B)
    'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y'   # 45-53: Abajo (D)
)

def r(offset):
    # Rotar cara 90 grados horario
    return [
        offset + 6, offset + 3, offset + 0,
        offset + 7, offset + 4, offset + 1,
        offset + 8, offset + 5, offset + 2
    ]

def r_inv(offset):
    # Rotar cara 90 grados antihorario
    return [
        offset + 2, offset + 5, offset + 8,
        offset + 1, offset + 4, offset + 7,
        offset + 0, offset + 3, offset + 6
    ]

# Indices inmutables, para las posiciones
I = list(range(54))

PERMUTACIONES = {
    # X - Eje Horizontal (1: Top, 2: Mid, 3: Bottom)
    'X1R': I[:], 'X1L': I[:],
    'X2R': I[:], 'X2L': I[:],
    'X3R': I[:], 'X3L': I[:],
    # Y - Eje Vertical (1: Left, 2: Mid, 3: Right)
    'Y1U': I[:], 'Y1D': I[:],
    'Y2U': I[:], 'Y2D': I[:],
    'Y3U': I[:], 'Y3D': I[:],
    # Z - Eje Profundidad (1: Front, 2: Mid, 3: Back)
    'Z1R': I[:], 'Z1L': I[:],
    'Z2R': I[:], 'Z2L': I[:],
    'Z3R': I[:], 'Z3L': I[:]
}

# TODO: Fill permutations...

class Nodo:
    def __init__(self, estado, padre=None, movimiento=None):
        self.estado = estado
        self.padre = padre
        self.movimiento = movimiento
    
    def obtener_camino(self):
        camino = []
        nodo_actual = self
        while nodo_actual.padre is not None:
            camino.append(nodo_actual.movimiento)
            nodo_actual = nodo_actual.padre
        return camino[::-1]

def aplicar_movimiento(estado, movimiento):
    p = PERMUTACIONES[movimiento]
    return tuple(estado[i] for i in p)

def BFS(estado_inicial):
    if estado_inicial == ESTADO_RESUELTO:
        return []

    Q = deque([Nodo(estado_inicial)])
    visitados = {estado_inicial}
    
    movimientos = list(PERMUTACIONES.keys())
    
    while Q:
        actual = Q.popleft()
        
        for mov in movimientos:
            nuevo_estado = aplicar_movimiento(actual.estado, mov)
            if nuevo_estado == ESTADO_RESUELTO:
                hijo = Nodo(nuevo_estado, padre=actual, movimiento=mov)
                return hijo.obtener_camino()
                
            if nuevo_estado not in visitados:
                visitados.add(nuevo_estado)
                Q.append(Nodo(nuevo_estado, padre=actual, movimiento=mov))
    return None
