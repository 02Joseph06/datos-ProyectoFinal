from algoritmo_rubik_final import ESTADO_RESUELTO, aplicar_movimiento, bfs_resolver_rubik

def main():
    print("=== TESTEADOR ALGORITMO NORMAL (LOGICA PURA) ===")
    
    # 1. Creamos un cubo resuelto y lo desordenamos nosotros mismos.
    cubo_test = ESTADO_RESUELTO
    
    # Elegir aleatoriamente algunos movimientos para mezclarlo
    scramble = ["X1R", "Y1U", "Z3L"] 
    
    print(f"-> Desordenando cubo con: {' '.join(scramble)}")
    for mov in scramble:
        cubo_test = aplicar_movimiento(cubo_test, mov)
        
    # 2. Le pasamos el cubo matemático roto al resolvedor
    print("-> Analizando ruta de resolucion en memoria RAM...")
    
    # Restringimos a los 12 ejes externos que usamos en Minecraft para imitar esa busqueda rapida
    movs_externos = [
        "X1R", "X1L", "X3R", "X3L", 
        "Y1U", "Y1D", "Y3U", "Y3D",
        "Z1R", "Z1L", "Z3R", "Z3L"
    ]
    
    solucion = bfs_resolver_rubik(cubo_test, movs_externos)
    
    # 3. Imprimimos el resultado final
    if solucion is not None:
        print("\n¡Exito! Se encontro una solucion.")
        print(f"Pasos necesarios ({len(solucion)} movimientos): {' -> '.join(solucion)}")
    else:
        print("\nFalla: El limite de 100,000 nodos se rebaso o no hay solucion posible (cubo imposible matematicamente).")

if __name__ == "__main__":
    main()