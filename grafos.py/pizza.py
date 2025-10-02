"""
PROGRAMA: BUSCADOR DE COMIDAS SIMILARES CON GRAFO
AUTOR: Hector Pesquera
FECHA: 02/10/25

DESCRIPCIÓN:
Este programa es un buscador de comidas similares que compara distintos platos según sus atributos principales
como el tipo de comida, color, ingrediente base y estilo culinario. A partir de estos criterios calcula un porcentaje 
de similitud entre cada par de comidas, donde valores altos indican mayor parecido. Por ejemplo, 
una Pizza margarita y unos Spaghetti boloñesa resultan bastante parecidos porque ambos son platos 
principales, de estilo italiano y con colores similares, obteniendo un 70 % de similitud; en cambio,
la Pizza margarita y la Ensalada verde apenas alcanzan un 22 % porque tienen distinto tipo, ingredientes y colores. 
Los resultados se muestran en forma de lista y también en un grafo, donde cada nodo es una comida y las conexiones 
representan el grado de similitud entre ellas.

EJEMPLO DE USO:
- Si buscas "Pizza margarita", el programa te dirá que es similar a 
  "Spaghetti boloñesa" (ambas italianas) y te mostrará un 85% de similitud.
"""

# Importamos librerías necesarias
import math                    # Para cálculos matemáticos (ej: raíz cuadrada en distancias de color)
import networkx as nx          # Para crear y manipular grafos (nodos, aristas, pesos, layouts)
import matplotlib.pyplot as plt # Para visualizar el grafo en pantalla

# -----------------------
# LISTA DE COMIDAS (NODOS)
# -----------------------
# Cada comida se representa con un diccionario de atributos:
# - nombre: cómo se llama el plato
# - tipo: si es principal, entrada, etc.
# - color: color principal representado en código HEX
# - ingrediente: ingrediente clave de la comida
# - estilo: estilo culinario (italiano, japonés, etc.)
comidas = [
    {"nombre": "Pizza margarita", "tipo": "principal", "color": "#FF4500", "ingrediente": "harina", "estilo": "italiano"},
    {"nombre": "Hamburguesa clásica", "tipo": "principal", "color": "#8B4513", "ingrediente": "carne", "estilo": "americano"},
    {"nombre": "Sushi de salmón", "tipo": "principal", "color": "#FFA07A", "ingrediente": "pescado", "estilo": "japonés"},
    {"nombre": "Ensalada verde", "tipo": "entrada", "color": "#008000", "ingrediente": "vegetales", "estilo": "saludable"},
    {"nombre": "Spaghetti boloñesa", "tipo": "principal", "color": "#FF6347", "ingrediente": "pasta", "estilo": "italiano"},
    {"nombre": "Tacos mexicanos", "tipo": "principal", "color": "#FFD700", "ingrediente": "maíz", "estilo": "mexicano"}
]

# FUNCIONES DE AYUDA

# Convierte un color en HEX (ej: "#FF4500") a una tupla RGB (ej: (255, 69, 0))
def hex_a_rgb(hex_color):
    hex_color = hex_color.lstrip('#')  # Elimina el carácter "#" al inicio
    # Convierte cada par de dígitos hexadecimales en un número decimal (0-255)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Calcula la distancia entre dos colores en el espacio RGB usando distancia euclidiana
def diferencia_colores(c1, c2):
    rgb1 = hex_a_rgb(c1)  # Convierte primer color a RGB
    rgb2 = hex_a_rgb(c2)  # Convierte segundo color a RGB
    # Distancia euclidiana: sqrt((R1-R2)^2 + (G1-G2)^2 + (B1-B2)^2)
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))

# Define un criterio de similitud entre estilos culinarios
def similitud_estilos(e1, e2):
    if e1 == e2:
        return 1.0  # Si son idénticos, similitud máxima
    # Pares de estilos que consideramos "relativamente similares"
    combinaciones = [("italiano", "saludable"), ("americano", "mexicano")]
    for c in combinaciones:
        if e1 in c and e2 in c:
            return 0.7  # Similares, pero no idénticos
    return 0.3  # Poco parecidos

# CÁLCULO DE SIMILITUD

# Devuelve un valor de similitud (0 a 1) entre dos comidas en base a sus atributos
def calcular_similitud(c1, c2):
    puntos = 0
    total = 4  # Número de criterios a evaluar: tipo, color, ingrediente, estilo

    # Si el tipo de plato es igual, suma 1 punto
    if c1["tipo"] == c2["tipo"]:
        puntos += 1

    # Comparación de colores (cuanto menor sea la diferencia, más puntos se suman)
    diff = diferencia_colores(c1["color"], c2["color"])
    # Normalizamos dividiendo entre 442 (máxima diferencia posible) para obtener valor entre 0 y 1
    puntos += max(0, 1 - diff / 442)

    # Si el ingrediente principal coincide, suma 1 punto
    if c1["ingrediente"] == c2["ingrediente"]:
        puntos += 1

    # Evalúa la similitud de estilos (entre 0.3 y 1 según la función anterior)
    puntos += similitud_estilos(c1["estilo"], c2["estilo"])

    # Divide entre el total de criterios para obtener porcentaje de similitud
    return puntos / total

# FUNCIÓN: BUSCAR SIMILARES

# Busca las comidas más parecidas a la comida introducida por nombre
def encontrar_similares(nombre, lista, top_n=3):
    buscada = None
    # Busca en la lista el diccionario de la comida cuyo "nombre" coincida
    for c in lista:
        if c["nombre"].lower() == nombre.lower():
            buscada = c
            break
    if buscada is None:  # Si no se encuentra el plato
        print(f"No encontré '{nombre}' en la lista.")
        return []
    
    resultados = []
    # Recorre todos los demás platos y calcula su similitud con la buscada
    for c in lista:
        if c["nombre"] != buscada["nombre"]:  # Evita compararla consigo misma
            sim = calcular_similitud(buscada, c)
            resultados.append((c["nombre"], sim))
    
    # Ordena resultados de mayor a menor similitud
    resultados.sort(key=lambda x: x[1], reverse=True)
    return resultados[:top_n]  # Devuelve solo los N más parecidos

# CONSTRUCCIÓN GRAFO

def construir_grafo(lista):
    G = nx.Graph()  # Crea un grafo vacío no dirigido
    # Añade cada comida como nodo
    for c in lista:
        G.add_node(c["nombre"])
    # Añade aristas entre cada par de comidas con un peso = similitud
    for i in range(len(lista)):
        for j in range(i+1, len(lista)):
            sim = calcular_similitud(lista[i], lista[j])
            if sim > 0:  # Solo si hay alguna similitud
                G.add_edge(lista[i]["nombre"], lista[j]["nombre"], weight=sim)
    return G

# DIBUJAR EL GRAFO

def dibujar_grafo(G):
    pos = nx.spring_layout(G)  # Calcula posiciones de nodos automáticamente
    pesos = nx.get_edge_attributes(G, 'weight')  # Obtiene pesos de las aristas
    # Dibuja nodos y nombres
    nx.draw(G, pos, with_labels=True, node_color="lightcoral", node_size=2000, font_size=8)
    # Dibuja etiquetas en las aristas mostrando el peso con 2 decimales
    nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{v:.2f}" for k,v in pesos.items()})
    plt.show()  # Muestra la figura

# PROGRAMA PRINCIPAL

print("=== BUSCADOR DE COMIDAS SIMILARES ===")
print("Comidas disponibles:")
# Muestra la lista de comidas con numeración
for i, c in enumerate(comidas, 1):
    print(f"{i}. {c['nombre']}")

# Bucle principal para interactuar con el usuario
while True:
    entrada = input("\nEscribe el nombre de la comida (o 'salir' para terminar): ")
    if entrada.lower() == "salir":
        print("¡Adiós!")
        break
    # Encuentra comidas similares a la elegida
    similares = encontrar_similares(entrada, comidas)
    if similares:
        print(f"\nComidas más similares a '{entrada}':")
        for nombre, sim in similares:
            print(f"- {nombre} ({sim*100:.1f}% similar)")

# Construye y dibuja el grafo al terminar
G = construir_grafo(comidas)
dibujar_grafo(G)
