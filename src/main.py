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
import time
from typing import Tuple
import matplotlib.pyplot as plt

Tiempo_a_demorar = 10

def metodoEulerRecursivo(f, xi:float, yi:float, xf:float, intervalo:float)-> list[Tuple[float, float]]:
    # Caso base
    plt.plot([xi, xi + intervalo], [yi, yi + intervalo * f(xi, yi)], marker='o', linestyle='-', color='r')
    plt.pause(Tiempo_a_demorar/cantIntervalos)  # Pausa para actualizar el gráfico
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
    if(x<=areaInicial):
        return areaInicial
    elif(x>areaInicial and x<=areaFinal):
        return(x)
    elif(x>areaFinal):
        return areaFinal

def A_derivada(x: float) -> float:
    if(x<=areaInicial):
        return 0
    elif(x>areaInicial and x<=areaFinal):
        return(1)
    elif(x>areaFinal):
        return 0

# Parámetros iniciales
xi = 0.0  # valor inicial de x
xf = 2 * areaInicial + areaFinal # valor final de x 
Pi = 340000.0  # valor inicial de la presion
delta_x = 0.05
intervalo = areaInicial* delta_x  # tamaño del paso
cantIntervalos = (xf - xi)/intervalo

plt.figure(figsize=(10, 6))
plt.xlabel('x')
plt.ylabel('P(x)')
plt.title('Presión en función de la distancia')
plt.grid(True)

metodoEulerRecursivo(f, xi, Pi, xf, intervalo)
plt.show()
