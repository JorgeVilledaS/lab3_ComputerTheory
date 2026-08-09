"""
Laboratorio No. 3 - Ejercicio 1
Convierte expresiones regulares de infix a postfix (Shunting Yard) y
luego construye y dibuja el Árbol de Sintaxis Abstracta (AST) de cada expresión.

Autor: Jorge Villeda 24932 y Lázaro Díaz 24713
"""

import matplotlib.pyplot as plt

# Caracteres que NO son literales (son operadores o símbolos especiales)
OPERADORES = set("()|*+?.")

# Precedencia de los operadores (mayor número = mayor precedencia)
PRECEDENCIA = {"|": 1, ".": 2, "*": 3, "+": 3, "?": 3}


class Nodo:
    """Representa un nodo del árbol de sintaxis abstracta (AST)."""

    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho


def es_literal(caracter):
    """Determina si un caracter es un símbolo del alfabeto (no un operador)."""
    return caracter not in OPERADORES


def insertar_concatenacion(regex):
    """Inserta el operador explícito de concatenación '.' donde corresponda."""
    resultado = []
    for i, actual in enumerate(regex):
        resultado.append(actual)
        if i + 1 < len(regex):
            siguiente = regex[i + 1]
            actual_termina_operando = es_literal(actual) or actual in ")*+?"
            siguiente_inicia_operando = es_literal(siguiente) or siguiente == "("
            if actual_termina_operando and siguiente_inicia_operando:
                resultado.append(".")
    return "".join(resultado)


def shunting_yard(regex):
    """Convierte una expresión regular de notación infix a postfix."""
    salida = []
    pila_operadores = []

    for token in regex:
        if es_literal(token):
            salida.append(token)
        elif token == "(":
            pila_operadores.append(token)
        elif token == ")":
            while pila_operadores[-1] != "(":
                salida.append(pila_operadores.pop())
            pila_operadores.pop()  # descarta el '('
        else:  # es un operador: |, ., *, +, ?
            while (pila_operadores and pila_operadores[-1] != "(" and
                   PRECEDENCIA.get(pila_operadores[-1], 0) >= PRECEDENCIA.get(token, 0)):
                salida.append(pila_operadores.pop())
            pila_operadores.append(token)

    while pila_operadores:
        salida.append(pila_operadores.pop())

    return salida


def copiar_arbol(nodo):
    """Crea una copia profunda de un subárbol (necesario para expandir a+)."""
    if nodo is None:
        return None
    return Nodo(nodo.valor, copiar_arbol(nodo.izquierdo), copiar_arbol(nodo.derecho))


def construir_arbol(postfix):
    """
    Construye el AST a partir de la expresión postfix usando una pila.
    Además simplifica las extensiones:
        a+  ->  a . a*
        a?  ->  a | ε
    """
    pila = []

    for token in postfix:
        if token in ("|", "."):
            derecho = pila.pop()
            izquierdo = pila.pop()
            pila.append(Nodo(token, izquierdo, derecho))

        elif token == "*":
            operando = pila.pop()
            pila.append(Nodo("*", operando))

        elif token == "+":
            # a+  equivale a  a . a*
            operando = pila.pop()
            estrella = Nodo("*", copiar_arbol(operando))
            pila.append(Nodo(".", operando, estrella))

        elif token == "?":
            # a?  equivale a  a | ε
            operando = pila.pop()
            epsilon = Nodo("ε")
            pila.append(Nodo("|", operando, epsilon))

        else:  # literal (a, b, 0, 1, ε, etc.)
            pila.append(Nodo(token))

    return pila.pop()


def asignar_posiciones(nodo, profundidad, contador_x, posiciones):
    """
    Recorre el árbol y calcula una posición (x, y) para cada nodo.
    - La 'y' depende de la profundidad (nivel) del nodo.
    - La 'x' de las hojas se asigna en orden (izquierda a derecha) y la
      'x' de los nodos internos es el promedio de sus hijos, para que el
      árbol quede centrado y ordenado.
    """
    if nodo.izquierdo is None and nodo.derecho is None:
        x = contador_x[0]
        contador_x[0] += 1
        posiciones[nodo] = (x, -profundidad)
        return

    if nodo.izquierdo is not None:
        asignar_posiciones(nodo.izquierdo, profundidad + 1, contador_x, posiciones)
    if nodo.derecho is not None:
        asignar_posiciones(nodo.derecho, profundidad + 1, contador_x, posiciones)

    xs_hijos = []
    if nodo.izquierdo is not None:
        xs_hijos.append(posiciones[nodo.izquierdo][0])
    if nodo.derecho is not None:
        xs_hijos.append(posiciones[nodo.derecho][0])

    posiciones[nodo] = (sum(xs_hijos) / len(xs_hijos), -profundidad)


def dibujar_conexiones(nodo, posiciones, ejes):
    """Dibuja las líneas (aristas) entre cada nodo y sus hijos."""
    x1, y1 = posiciones[nodo]
    for hijo in (nodo.izquierdo, nodo.derecho):
        if hijo is not None:
            x2, y2 = posiciones[hijo]
            ejes.plot([x1, x2], [y1, y2], color="black", linewidth=1.5, zorder=1)
            dibujar_conexiones(hijo, posiciones, ejes)


def dibujar_arbol(raiz, nombre_archivo):
    """Dibuja el árbol completo usando matplotlib y lo guarda como imagen PNG."""
    posiciones = {}
    asignar_posiciones(raiz, profundidad=0, contador_x=[0], posiciones=posiciones)

    xs = [pos[0] for pos in posiciones.values()]
    ys = [pos[1] for pos in posiciones.values()]
    ancho = max(xs) - min(xs) + 2
    alto = max(ys) - min(ys) + 2

    figura, ejes = plt.subplots(figsize=(max(ancho * 0.9, 4), max(alto * 1.2, 3)))

    # Primero las líneas, para que queden detrás de los círculos
    dibujar_conexiones(raiz, posiciones, ejes)

    radio = 0.3
    for nodo, (x, y) in posiciones.items():
        circulo = plt.Circle((x, y), radio, facecolor="white", edgecolor="black", zorder=2)
        ejes.add_patch(circulo)
        ejes.text(x, y, nodo.valor, ha="center", va="center", fontsize=13, zorder=3)

    ejes.set_xlim(min(xs) - 1, max(xs) + 1)
    ejes.set_ylim(min(ys) - 1, max(ys) + 1)
    ejes.set_aspect("equal")
    ejes.axis("off")

    figura.tight_layout()
    figura.savefig(f"{nombre_archivo}.png", dpi=150)
    plt.close(figura)


def procesar_expresion(regex_original, indice):
    """Ejecuta el proceso completo para una expresión regular: infix -> postfix -> AST -> imagen."""
    print(f"Expresión original : {regex_original}")

    regex_con_concat = insertar_concatenacion(regex_original)
    print(f"Con concatenación  : {regex_con_concat}")

    postfix = shunting_yard(regex_con_concat)
    print(f"Notación postfix   : {''.join(postfix)}")

    arbol = construir_arbol(postfix)

    nombre_archivo = f"arbol_{indice}"
    dibujar_arbol(arbol, nombre_archivo)
    print(f"Árbol guardado en  : {nombre_archivo}.png\n")


def main():
    with open("expresiones.txt", "r", encoding="utf-8") as archivo:
        lineas = [linea.strip() for linea in archivo if linea.strip()]

    for indice, regex_original in enumerate(lineas, start=1):
        procesar_expresion(regex_original, indice)


if __name__ == "__main__":
    main()