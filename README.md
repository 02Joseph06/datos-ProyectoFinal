# 🧩 Proyecto Rubik-Minecraft Automatizado

Este proyecto representa una impresionante supercomputadora matemática capaz de leer, analizar y resolver un Cubo de Rubik 3x3x3 físico — construido artificialmente bloque a bloque con pura ingeniería de Redstone — operando directamente dentro del entorno y las físicas del mundo de Minecraft.

Combina un potente motor algebraico escrito en Python para simular movimientos geométricos mediante transformaciones abstractas de matrices y grafos. Esta abstracción mental del cubo se comunica sin interrupciones con actuadores físicos mediante inyección de comandos en tiempo real, conectando así una lógica matemática invisible con pistones mecánicos gigantescos dentro del juego.

---

# 🧩 Participantes:

Sebastian Garcia,
Juan Holguin,
Samuel Moya,
Luigi Rincon.

## 🧠 Parte 1: El Modelo Matemático y Lógica Estructural del Algoritmo

Para que el algoritmo Python resuelva los trillones de combinaciones del Cubo de Rubik con extrema rapidez y bajo costo computacional, desechamos la idea natural de renderizar el objeto 3D en la memoria, ya que trazar cada cara, vértice y arista tridimensional es dolorosamente lento. En lugar de eso, el cubo fue "aplastado" conceptualmente bajo matrices de estado lineales.

### La Representación del Estado (Array o Tupla 1D)
El famoso cubo de Rubik tradicional de 3x3x3 consta de 6 caras diferentes, donde cada una exhibe 9 bloques de un color específico. En lugar de manejar una pesada y engorrosa matriz anidada del estilo `[cara][x][y]`, hemos "desplegado" las caras del cubo imaginando una cruz plana (como la vista de una caja de cartón desarmada) conteniendo así **54 elementos en un simple listado unidimensional**. 

La matemática lo etiqueta de esta forma por orden estricto de escaneo:
1. **Arriba (Up) - `W`** (Índices [0 al 8])
2. **Izquierda (Left) - `G`** (Índices [9 al 17])
3. **Frente (Front) - `R`** (Índices [18 al 26])
4. **Derecha (Right) - `B`** (Índices [27 al 35])
5. **Atrás (Back) - `O`** (Índices [36 al 44])
6. **Abajo (Down) - `Y`** (Índices [45 al 53])

*¿Por qué se optó por la estructura `Tuple` (Tupla) en Python?*  
Las listas tradicionales consumen procesamiento, sin embargo, en Python, una vez que encerramos esos 54 datos en una Tupla inmutable, el compilador puede generar una firma unívoca por "hash". Es decir, convertimos la disposición de los colores en un tipo de "código de barras matemático". Cuando el programa inspecciona millones de combinaciones y se topa con un código de barras que ya visitó anteriormente, su diccionario interno (`set()`) le avisa instantáneamente descartándolo con una asombrosa eficiencia de **O(1) en tiempo**, esquivando así costosos chequeos redundantes de procesamiento.

### Álgebra de Rotación: El Motor Criptográfico del Movimiento
Para manipular esta tupla, el algoritmo se centra en puro desplazamiento y permutaciones de índices (jugar a saltar posiciones). Al solicitar rotar un "eje", como la capa Frontal (Z3) o la de Arriba (X1), el código disecciona el movimiento en dos pasos quirúrgicos:

1. **Translación de Bordes Perimetrales**: Al mover el tercio superior de un cubo real, el borde visual superior de Izquierda se traslada y expulsa hacia el Frente, el Frente hacia la Derecha, Derecha a Atrás, etc. Para programar esto, se seleccionan 4 rodajas adyacentes de 3 índices de distancia, y sistemáticamente sobrescribimos el `array[A]` con la memoria almacenada temporalmente de `array[B]`. Si la traslación es de tipo `R` o de tipo `L`, simplemente se invierte el orden del remplazo. 
2. **Rotación Unipolar Planar**: Las caras centrales impactadas durante el movimiento no solo cambian bordes, la "tapa" o cara de 9 bloques enteramente visible tiene que girar 90º. Diseñamos funciones matriciales de reacomodo (`rotar_cara_horario` y su contraparte `rotar_cara_antihorario`). Los índices que formaban las esquinas se cambian de rincón transponiendo sus valores.

---

## 🔍 Parte 2: El Cerebro del Proyecto: Algoritmo de Búsqueda (BFS)

El núcleo algorítmico, encargado de desentrañar el rompecabezas de las permutaciones aplicadas y buscar el regreso óptimo, depende de un potente algoritmo de navegación profunda: **Búsqueda en Anchura (Breadth-First Search o BFS)**, conocido por encontrar invariablemente los "caminos más cortos" en un grafo.

### ¿Cómo evalúa el BFS los estados?
1. Se inicializa desplegando el estado caótico del cubo real extraído de Minecraft como su **"Nodo Raíz"**, marcando una latencia de 0 movimientos.
2. A este nodo se le aplican *en bucle paralelo* todas las operaciones que tu cuerpo de pistones autoriza (caras externas). Este lote produce 12 ramificaciones posibles, almacenadas para conformar el **Nivel 1** del árbol de permutaciones.
3. Lo mágico del algoritmo en Anchura — y que nos diferencia del recorrido en Profundidad (DFS) — es que BFS verificará cautelosamente cada una de estas 12 variantes de manera uniforme. Si ninguna recrea los patrones dictados del cubo `ESTADO_RESUELTO`, prosigue expandiendo uniformemente hacia la siguiente fase: derivando la matemática a **144 variantes de Nivel 2**, y así sucesivamente.

### Protecciones al Desbordamiento de RAM y la magia del DEQUE
Al manejar combinaciones exponenciales, computar "arrays" sobre la RAM tradicional provocaría parálisis total del sistema.
* Incorporamos `collections.deque()`; a nivel de ensamblador funciona usando una lista doblemente enlazada, permitiendo extraer cálculos procesados en la parte frontal de millones de datos al paso frenético de O(1). ¡Velocidad inigualable comparada al uso de "listas `.pop(0)`" normales!
* Añadimos estratégicamente el cordón o tope virtual paramétrico `LIMITE_SEGURO_NODOS = 50,000 / 100,000`. Esto es oro puro. Los bloques ubicados erróneamente en el juego (glitches visuales) crean estados matemáticamente "fantasmas" y fracturados. Este candado audita proactivamente la sobrecarga y cancela graciosamente la búsqueda antes de un colapso "Out Of Memory", informando que el cubo físico tiene una perturbación estructural letal.

---

## ⛏️ Parte 3: Fusión Extrema: Integración de Software a Hardware en Minecraft

Al ser un cálculo cerebral "puro", este debía incrustarse en el juego directamente para comandar los bloques de construcción de redstone.

### Lectura Perimetral de Vectores del Entorno
Nuestro código usa la cuadrícula tridimensional de coordenadas absolutas estocásticamente quemadas bajo la lista `COORDS_BLOQUES`. Usando la API, escaneamos 54 "pixels de concreto" ubicados en el juego, y a través de un filtrado mapeamos dinámicamente "minecraft:yellow_concrete" a letras matemáticas operacionales limpias como `Y`. 

### Controlador Remoto de Acciones (SetBlock)
Al dar con la gloriosa "receta" resultante de retrospección proporcionada por el BFS (Ej: `X1R -> Y3U -> Z3L`), convertimos la notación matemática final en espasmos programados de `/setblock`. Colocamos redstone momentánea a coordenadas adyacentes y la destruimos 0.5s después usando latencias `time.sleep()`. Este minucioso temporizado imita a la perfección una mano humana operando mandos físicos.

### La Obra de Arte "Physical Override" (`PHYSICAL_OVR`)
A veces "las tuercas giran suelto" en Minecraft y los redstoners instalan mecanismos que empujan en la dirección contraria. Alterar la pura matriz Python del algoritmo abstracto por culpa de un pistón físico trabado destruiría matemáticamente el cerebro por completo. Así que implementamos nuestra **Capa de Hardware Falso (`PHYSICAL_OVR`)**, cuyo único propósito es engañar. Si el cerebro dictamina matemáticamente girar "Y1U" (Un polo), pero el traductor sabe que tu empalme gira reverso de fábrica, manda sublimemente tu señal real hacia "Y1D" solucionando la avería física en tiempo real. 

---

## 🌟 Créditos 


* **Universidad Sergio Arboleda - Estructura de datos lineales**: **[Data Structures Linear / Final Project (GitHub de @memoodm)](https://github.com/memoodm/data-structures-linear/tree/main/final%20project)**, Provee los lineamientos críticos en Python, grafos, tuplas inmutables y el árbol de soluciones sobre cómo mapear el cubo sin las cuales la red de BFS no podría expandirse ágil y sanamente.

* **Minescript Framework Mod**:  Mod utilizado para la capa de conexion entre Minecraft y Python

* **RadiantInferno**: Credutis por haber creado el mapa con el sistema del cubo rubik recreado gracias al mod de Create.
