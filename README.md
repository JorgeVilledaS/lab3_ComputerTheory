# Laboratorio No. 3 – Ejercicio 1: Infix → Postfix → AST

Este programa toma expresiones regulares en notación **infix**, las convierte a
**postfix** usando el algoritmo de **Shunting Yard**, y con esa notación postfix
construye el **Árbol de Sintaxis Abstracta (AST)** correspondiente, dibujándolo
como una imagen.

## ¿Cómo funciona?

El proceso se hace en 4 pasos, uno por cada expresión regular leída del archivo
`expresiones.txt`:

1. **Insertar concatenación explícita**
   Se recorre la expresión y se agrega un operador `.` en los lugares donde hay
   una concatenación implícita (por ejemplo `ab` se convierte en `a.b`).

2. **Shunting Yard (infix → postfix)**
   Se usa una pila para reordenar los operadores según su precedencia:
   - `*`, `+`, `?` (mayor precedencia)
   - `.` (concatenación)
   - `|` (unión, menor precedencia)

3. **Construcción del AST**
   Se recorre la expresión postfix con una pila de nodos:
   - Si el token es un literal (`a`, `b`, `0`, `1`, `ε`), se crea un nodo hoja.
   - Si es `|` o `.`, se sacan dos nodos de la pila y se crea un nodo binario.
   - Si es `*`, se saca un nodo y se crea un nodo unario (Kleene star).
   - Si es `+`, se **simplifica** como `a.a*` (se saca el nodo, se hace una
     copia y se arma un nodo de concatenación con una estrella de la copia).
   - Si es `?`, se **simplifica** como `a|ε` (se saca el nodo y se arma un
     nodo de unión con un nodo epsilon).

4. **Dibujar el árbol**
   Se calcula una posición (x, y) para cada nodo del AST:
   - Las hojas se ordenan de izquierda a derecha.
   - Cada nodo interno se ubica en el promedio de la posición de sus hijos.
   - La altura (eje y) depende del nivel/profundidad del nodo.

   Con esas posiciones, se dibujan círculos (con `matplotlib.patches.Circle`)
   y líneas entre cada nodo y sus hijos, y se exporta todo como imagen `.png`.

## Tecnologías usadas

- **Python 3**
- **Matplotlib** para dibujar el árbol de sintaxis (no requiere instalar
  ningún programa externo, solo `pip install matplotlib`).

## Archivos

- `main.py` – Código fuente del programa.
- `expresiones.txt` – Archivo de entrada con las 4 expresiones regulares del
  laboratorio (una por línea).
- `arbol_1.png`, `arbol_2.png`, `arbol_3.png`, `arbol_4.png` – Árboles
  generados para cada expresión (se generan al ejecutar el programa).

## Instalación

```bash
pip install matplotlib
```

No se necesita instalar ningún programa adicional en el sistema operativo.

## Ejecución

```bash
python3 main.py
```

El programa imprime en consola, para cada expresión:
- La expresión original.
- La expresión con concatenación explícita.
- La notación postfix.
- El nombre del archivo de imagen generado con el árbol.

## Expresiones regulares procesadas

1. `(a*|b*)+`
2. `((ε|a)|b*)*`
3. `(a|b)*abb(a|b)*`
4. `0?(1?)?0*`

## Video

[Enlace al video de YouTube (no listado)](https://www.youtube.com/watch?v=vsAXXi5x8RA)
