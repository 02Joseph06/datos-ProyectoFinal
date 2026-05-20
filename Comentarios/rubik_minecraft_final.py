import time
from collections import deque
import minescript

# 1. Coordenadas de los bloques redstone (Pistones/Mecanismos).
COORDS_MECANISMOS = {
    "X1R": (306, 102, 199),
    "X3R": (306, 102, 197),
    "X1L": (305, 102, 199),
    "X3L": (305, 102, 197),
    "Y1U": (306, 102, 203),
    "Y3U": (306, 102, 201),
    "Y1D": (305, 102, 203),
    "Y3D": (305, 102, 201),
    "Z1R": (306, 102, 207),
    "Z3R": (306, 102, 205),
    "Z1L": (305, 102, 207),
    "Z3L": (305, 102, 205)
}

# 2. Diccionario Concreto -> Color Algoritmico.
MAPA_COLORES = {
    "minecraft:white_concrete": "W",   
    "minecraft:lime_concrete": "G",   
    "minecraft:red_concrete": "R",     
    "minecraft:blue_concrete": "B",    
    "minecraft:orange_concrete": "O",  
    "minecraft:yellow_concrete": "Y"   
}

# 3. Mapeo de escaneo ordenado en la misma cascada 1D: Arriba, Izquierda, Frente, Derecha, Atras, Abajo.
COORDS_BLOQUES = [
    [326, 96, 202], [326, 96, 198], [326, 96, 194],
    [330, 96, 202], [330, 96, 198], [330, 96, 194],
    [334, 96, 202], [334, 96, 198], [334, 96, 194],
    
    [326, 94, 204], [330, 94, 204], [334, 94, 204],
    [326, 90, 204], [330, 90, 204], [334, 90, 204], 
    [326, 86, 204], [330, 86, 204], [334, 86, 204],

    [336, 94, 202], [336, 94, 198], [336, 94, 194],
    [336, 90, 202], [336, 90, 198], [336, 90, 194], 
    [336, 86, 202], [336, 86, 198], [336, 86, 194],

    [334, 94, 192], [330, 94, 192], [326, 94, 192],
    [334, 90, 192], [330, 90, 192], [326, 90, 192],
    [334, 86, 192], [330, 86, 192], [326, 86, 192],

    [324, 94, 194], [324, 94, 198], [324, 94, 202],
    [324, 90, 194], [324, 90, 198], [324, 90, 202],
    [324, 86, 194], [324, 86, 198], [324, 86, 202],

    [334, 84, 202], [334, 84, 198], [334, 84, 194],
    [330, 84, 202], [330, 84, 198], [330, 84, 194],
    [326, 84, 202], [326, 84, 198], [326, 84, 194]
]

# 4. Plantilla de comparacion resolutiva.
ESTADO_RESUELTO = (
    'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W',  
    'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',  
    'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R',  
    'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B',  
    'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',  
    'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y'   
)

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


# 5. Core de resolucion (Busqueda en Anchura / BFS).
# Garantiza la via mas corta procesando movimientos nivel a nivel mediante una cola FIFO (deque).
def bfs_resolver_rubik(estado_inicial):
    if estado_inicial == ESTADO_RESUELTO:
        return []

    frontera = deque([Nodo(estado_inicial)])
    visitados = set([estado_inicial]) # Hash rápido para descartar ciclos y estados duplicados en tiempo O(1).
    
    minescript.echo("Iniciando busqueda BFS pura en memoria...")
    
    # Filtramos la profundidad a unicamente hardware disponible.
    movimientos = list(COORDS_MECANISMOS.keys())
    
    nodos_expl = 0
    LIMITE_SEGURO_NODOS = 50000 # Evita Out of Memory Error si el hardware falló antes.
    
    while frontera:
        nodo_actual = frontera.popleft()
        nodos_expl += 1
        
        if nodos_expl % 5000 == 0:
            minescript.echo(f"  -> Depurando: {nodos_expl} nodos explorados. Manteniendo memoria segura...")
            
        if nodos_expl > LIMITE_SEGURO_NODOS:
            minescript.echo(f"ERROR: BFS superó el limite ({LIMITE_SEGURO_NODOS} nodos).")
            minescript.echo("RAZÓN POSIBLE: El estado generó un patron imposible de bloques (Matematicamente irresoluble).")
            return None
            
        for mov in movimientos:
            nuevo_estado = aplicar_movimiento(nodo_actual.estado, mov)
            
            if nuevo_estado == ESTADO_RESUELTO:
                minescript.echo(f"¡Solucion encontrada! Nodos explorados: {nodos_expl}")
                return Nodo(nuevo_estado, padre=nodo_actual, movimiento=mov).obtener_camino()
                
            if nuevo_estado not in visitados:
                visitados.add(nuevo_estado)
                frontera.append(Nodo(nuevo_estado, padre=nodo_actual, movimiento=mov))
                
    return None

# 6. Salida de redstone.
def ejecutar_en_minecraft(camino):
    # Traductor de Hardware: Convierte el calculo correcto a la debilidad/inversion del mecanismo fisico real instalado en el mapa.
    PHYSICAL_OVR = {
        'X1L': 'X1R',
        'X1R': 'X1L',
        'Y1U': 'Y1D',
        'Y1D': 'Y1U',
        'Y3U': 'Y3D',
        'Y3D': 'Y3U',
        'Z1L': 'Z1R',
        'Z1R': 'Z1L',
        'Z3L': 'Z3R',
        'Z3R': 'Z3L'
    }
    
    for index, mov in enumerate(camino):
        mov_fisico = PHYSICAL_OVR.get(mov, mov) 
        minescript.echo(f"Paso {index + 1}/{len(camino)}: Ejecutando {mov} (Mandando señal física a {mov_fisico})")
        
        # Desencadenador redstone usando setblock
        x, y, z = COORDS_MECANISMOS[mov_fisico]
        minescript.execute(f"/setblock {x} {y} {z} redstone_block")
        time.sleep(0.5) # Pausas asincronas para hardware
        minescript.execute(f"/setblock {x} {y} {z} air")
        time.sleep(1.5)
        
    # Salida estetica final en chat de juego
    minescript.echo(f"=========================================")
    minescript.echo(f"¡Cubo resuelto!")
    minescript.echo(f"Historico de los pasos dados: {' -> '.join(camino)}")
    minescript.echo(f"=========================================")

# 7. Escaneo del mundo a la matriz de programacion.
# Mapea el volumen 3D del juego convirtiendolo en el vector 1D exacto a ESTADO_RESUELTO que inyectaremos en el BFS.
def leer_estado_cubo_minecraft():
    minescript.echo("Escaneando el estado del cubo físico...")
    estado_actual = []
    
    # Captura multi-bloques masiva instantanea.
    bloques_juego = minescript.getblocklist(COORDS_BLOQUES)
    
    for indice, bloque in enumerate(bloques_juego):
        # Filtrado de ID
        bloque_normalizado = bloque if bloque.startswith("minecraft:") else f"minecraft:{bloque}"
        
        # Traduccion
        if bloque_normalizado in MAPA_COLORES:
            estado_actual.append(MAPA_COLORES[bloque_normalizado])
        else:
            minescript.echo(f"Falla de escaneo: Bloque desconocido '{bloque}' detectado en indice {indice}")
            estado_actual.append('X')
            
    return tuple(estado_actual)

# 8. Loop principal de logica
if __name__ == "__main__":
    cubo_desordenado = leer_estado_cubo_minecraft()
    
    if 'X' in cubo_desordenado:
        minescript.echo("Error: Existen bloques leídos que no coinciden.")
    else:
        # Llamada motor BFS
        solucion = bfs_resolver_rubik(cubo_desordenado)
        
        if solucion is not None:
            minescript.echo(f"Camino planificado: {' '.join(solucion)}")
            # Envia la matriz lista a las fisicas de Minecraft
            ejecutar_en_minecraft(solucion)
        else:
            minescript.echo("El bucle terminó sin encontrar solución. Revisa la consola o escaneo, el cubo puede estar matemáticamente roto.")