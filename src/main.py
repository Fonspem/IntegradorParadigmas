"""
Paradigmas y Lenguajes de Programación I
1.	Crear una función recursiva que aplique el método de Euler para resolver la ecuación diferencial planteada.
2.	Graficar en tiempo real la solución a medida que se calculan los valores recursivamente.
3.	Utilizar nodos y estructuras de datos (por ejemplo, listas enlazadas) para almacenar los datos calculados.
4.	Mostrar los datos almacenados en un formato legible.
5.	Implementar un menú interactivo con las siguientes opciones:
    a.	Mostrar los datos calculados.
    b.	Ingresar una coordenada para el cálculo de error:
        i.	Ingresar tiempo y valor de la imagen.
        ii.	Graficar el punto en la gráfica.
        iii.	Realizar una búsqueda binaria en la lista para calcular el error entre el punto ingresado y el punto correspondiente en el tiempo dado.
        c.	Mostrar historial de coordenadas ingresadas y sus respectivos cálculos de error.c
    d.	Buscar un dato en la lista ingresando el tiempo.
    e.	Buscar un dato en la lista ingresando la variable dependiente o su valor más cercano.
    f.	Limpiar la consola.
    g.	Salir del programa.
6.	Comparar la solución aproximada obtenida por el método de Euler (implementada en el programa) con la solución analítica.
7.	Analizar y explicar las diferencias observadas entre ambas soluciones.
8.	Añadir cualquier otra función que consideres necesaria para mejorar la eficiencia o funcionalidad del programa.
"""

import math
from typing import Callable, Tuple

def metodoEulerRecursivo(f: Callable[[float, float], float], xi: float, yi: float,  xf: float,
                        intervalo: float)-> list[Tuple[float, float]]:
    # Caso base
    if xi >= xf:
        return [(xi, yi)]
    
    return [(xi, yi)] + metodoEulerRecursivo(f, xi + intervalo , yi + intervalo * f(xi, yi) , xf, intervalo)

rho = 1000 # kg/m^3 1000:H2O, 1,2:aire
areaInicial = 3.1415 * (0.03/2)**2 # m^2
areaFinal = 3.1415 * (0.05/2)**2 # m^2
velocidad = 3.0 #m/s
Caudal = areaInicial * velocidad #m^3/s

def f(x: float, p: float) -> float:
    return rho * (V(x, Caudal)**2 * A_derivada(x)) / A(x)

def V(x: float, Q: float) -> float:
    return (Q/A(x))



def A(x: float) -> float:
    #math.sin(x) + 2.7 * math.cos((x ** 2) / (2.7 * x)) + 5 es una funcion basztante aleatoria
    #return (math.sin(x) + 2)
    #return 0.2 + 0.1 * x

    if(x<=areaInicial):
        return areaInicial
    elif(x>areaInicial and x<=areaFinal):
        return(x)
    elif(x>areaFinal):
        return areaFinal

def A_derivada(x: float) -> float:
    #return (-math.cos(x))
    #return 0.1
    if(x<=areaInicial):
        return 0
    elif(x>areaInicial and x<=areaFinal):
        return(1)
    elif(x>areaFinal):
        return 0

# Parámetros iniciales
x0 = 0.0  # El valor inicial de x
y0 = 340000  # El valor inicial de 
x_end = 2 * areaInicial + areaFinal   # El valor final de x 0.00012665 * 2.5 para una manguera
step_size = areaInicial/10  # El tamaño del paso

# Resolver la ecuación diferencial usando el método de Euler recursivo
result = metodoEulerRecursivo(f, x0, y0, x_end, step_size)

# Imprimir los resultados
for (x, y) in result:
    print(f"x: {x:.2f}, y: {y:.2f}")


import matplotlib.pyplot as plt

# Datos proporcionados

# Separar los datos en listas de x y y
x_vals, y_vals = zip(*result)

# Crear la gráfica
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, marker='o', linestyle='-', color='b')

# Agregar etiquetas y título
plt.xlabel('x')
plt.ylabel('y')
plt.title('Gráfica de los datos proporcionados')
plt.grid(True)

# Mostrar la gráfica
plt.show()