from collections import deque

ESTADO_RESUELTO = (
    'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W',  
    'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',  
    'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R',  
    'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B',  
    'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',  
    'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y'   
)

MOVIMIENTOS = [
    "X1R", "X1L", "X2R", "X2L", "X3R", "X3L",
    "Y1U", "Y1D", "Y2U", "Y2D", "Y3U", "Y3D",
    "Z1R", "Z1L", "Z2R", "Z2L", "Z3R", "Z3L"
]

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

def rotar_cara_horario(estado, p):
    return [
        estado[p+6], estado[p+3], estado[p+0],
        estado[p+7], estado[p+4], estado[p+1],
        estado[p+8], estado[p+5], estado[p+2]
    ]

def rotar_cara_antihorario(estado, p):
    return [
        estado[p+2], estado[p+5], estado[p+8],
        estado[p+1], estado[p+4], estado[p+7],
        estado[p+0], estado[p+3], estado[p+6]
    ]

def aplicar_movimiento(es, mov):
    n = list(es)
    
    if mov in ("X1R", "X1L", "X2R", "X2L", "X3R", "X3L"):
        c = int(mov[1]) - 1
        idx_L = [9 + c*3 + i for i in range(3)]
        idx_F = [18 + c*3 + i for i in range(3)]
        idx_R = [27 + c*3 + i for i in range(3)]
        idx_B = [36 + c*3 + i for i in range(3)]
        
        dir = mov[2]
        if dir == 'L':
            for i in range(3):
                n[idx_L[i]] = es[idx_F[i]]
                n[idx_F[i]] = es[idx_R[i]]
                n[idx_R[i]] = es[idx_B[i]]
                n[idx_B[i]] = es[idx_L[i]]
        else: 
            for i in range(3):
                n[idx_R[i]] = es[idx_F[i]]
                n[idx_B[i]] = es[idx_R[i]]
                n[idx_L[i]] = es[idx_B[i]]
                n[idx_F[i]] = es[idx_L[i]]
                
        if mov == "X1L": n[0:9] = rotar_cara_horario(es, 0)
        elif mov == "X1R": n[0:9] = rotar_cara_antihorario(es, 0)
        elif mov == "X3L": n[45:54] = rotar_cara_antihorario(es, 45)
        elif mov == "X3R": n[45:54] = rotar_cara_horario(es, 45)

    elif mov in ("Y1U", "Y1D", "Y2U", "Y2D", "Y3U", "Y3D"):
        c = int(mov[1]) - 1
        idx_U = [0 + i*3 + c for i in range(3)]
        idx_F = [18 + i*3 + c for i in range(3)]
        idx_D = [45 + i*3 + c for i in range(3)]
        idx_B = [36 + (2-i)*3 + (2-c) for i in range(3)]
        
        dir = mov[2]
        if dir == 'U':
            for i in range(3):
                n[idx_B[i]] = es[idx_U[i]]
                n[idx_U[i]] = es[idx_F[i]]
                n[idx_F[i]] = es[idx_D[i]]
                n[idx_D[i]] = es[idx_B[i]]
        else:
            for i in range(3):
                n[idx_F[i]] = es[idx_U[i]]
                n[idx_D[i]] = es[idx_F[i]]
                n[idx_B[i]] = es[idx_D[i]]
                n[idx_U[i]] = es[idx_B[i]]
                
        if mov == "Y1U": n[9:18] = rotar_cara_antihorario(es, 9)
        elif mov == "Y1D": n[9:18] = rotar_cara_horario(es, 9)
        elif mov == "Y3U": n[27:36] = rotar_cara_horario(es, 27)
        elif mov == "Y3D": n[27:36] = rotar_cara_antihorario(es, 27)

    elif mov in ("Z1R", "Z1L", "Z2R", "Z2L", "Z3R", "Z3L"):
        c = int(mov[1]) - 1 
        idx_U = [0 + (2-c)*3 + i for i in range(3)]
        idx_R = [27 + i*3 + c for i in range(3)]
        idx_D = [45 + c*3 + (2-i) for i in range(3)]
        idx_L = [9 + (2-i)*3 + (2-c) for i in range(3)]
        
        dir = mov[2]
        if dir == 'R':
            for i in range(3):
                n[idx_R[i]] = es[idx_U[i]]
                n[idx_D[i]] = es[idx_R[i]]
                n[idx_L[i]] = es[idx_D[i]]
                n[idx_U[i]] = es[idx_L[i]]
        else:
            for i in range(3):
                n[idx_L[i]] = es[idx_U[i]]
                n[idx_D[i]] = es[idx_L[i]]
                n[idx_R[i]] = es[idx_D[i]]
                n[idx_U[i]] = es[idx_R[i]]
                
        if mov == "Z1R": n[18:27] = rotar_cara_horario(es, 18)
        elif mov == "Z1L": n[18:27] = rotar_cara_antihorario(es, 18)
        elif mov == "Z3R": n[36:45] = rotar_cara_antihorario(es, 36)
        elif mov == "Z3L": n[36:45] = rotar_cara_horario(es, 36)

    return tuple(n)


def bfs_resolver_rubik(estado_inicial, movimientos_validos=None):
    if estado_inicial == ESTADO_RESUELTO:
        return []
        
    if movimientos_validos is None:
        movimientos_validos = MOVIMIENTOS

    frontera = deque([Nodo(estado_inicial)])
    visitados = set([estado_inicial])
    
    nodos_expl = 0
    LIMITE_SEGURO_NODOS = 100000 
    
    while frontera:
        nodo_actual = frontera.popleft()
        nodos_expl += 1
            
        if nodos_expl > LIMITE_SEGURO_NODOS:
            return None
            
        for mov in movimientos_validos:
            nuevo_estado = aplicar_movimiento(nodo_actual.estado, mov)
            
            if nuevo_estado == ESTADO_RESUELTO:
                return Nodo(nuevo_estado, padre=nodo_actual, movimiento=mov).obtener_camino()
                
            if nuevo_estado not in visitados:
                visitados.add(nuevo_estado)
                frontera.append(Nodo(nuevo_estado, padre=nodo_actual, movimiento=mov))
                
    return None