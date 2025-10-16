import time

# Definición de la clase Nodo
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

# Recorrido en Preorden: Nodo - Izquierdo - Derecho
def recorrido_preorden(nodo):
    if nodo:
        print(nodo.valor, end=" ")
        recorrido_preorden(nodo.izquierdo)
        recorrido_preorden(nodo.derecho)

# Recorrido en Inorden: Izquierdo - Nodo - Derecho
def recorrido_inorden(nodo):
    if nodo:
        recorrido_inorden(nodo.izquierdo)
        print(nodo.valor, end=" ")
        recorrido_inorden(nodo.derecho)

# Recorrido en Postorden: Izquierdo - Derecho - Nodo    4 5 2 6 7 3 1
def recorrido_postorden(nodo):
    if nodo:
        recorrido_postorden(nodo.izquierdo)
        recorrido_postorden(nodo.derecho)
        print(nodo.valor, end=" ")

raiz = Nodo(1)
raiz.izquierdo = Nodo(2)
raiz.derecho = Nodo(3)
raiz.izquierdo.izquierdo = Nodo(4)
raiz.izquierdo.derecho = Nodo(5)
raiz.derecho.izquierdo = Nodo(6)
raiz.derecho.derecho = Nodo(7)
