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
from sympy import *
import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt

def metodoEulerRecursivo(f, xi:float, yi:float, xf:float, intervalo:float)-> list[Tuple[float, float]]:
    # Caso base
    plt.plot([xi, xi + intervalo], [yi, yi + intervalo * f(xi, yi)], marker='o', linestyle=' ', color='r')
    plt.pause(duracionGrafico/cantIntervalos)  # Pausa para actualizar el gráfico
    if xi >= xf:
        return [(xi, yi)]
    
    return [(xi, yi)] + metodoEulerRecursivo(f, xi + intervalo , yi + intervalo * f(xi, yi) , xf, intervalo)

X = Symbol("x")
media = 3.0
desvioEst = 0.6
DistNormal =  (exp(-0.5*((X-media)/desvioEst)**2)) / (sqrt(2 * pi) * desvioEst) 

Area = (2 * (1 - DistNormal))/2 * np.pi
Area_derivada = diff(Area, X)

def A(x: float) -> float:
    return Area.evalf(subs={X: x})

def A_derivada(x: float) -> float:
    return Area_derivada.evalf(subs={X: x})

rho = 1000 # kg/m^3 1000:H2O, 1,2:aire
areaInicial = A(0.0) # m^2
velocidad = 3.0 #m/s
Caudal = areaInicial * velocidad #m^3/s

def V(x: float, Q: float) -> float:
    return (Q/A(x))

def f(x: float, p: float) -> float:
    return rho * (V(x, Caudal)**2 * A_derivada(x)) / A(x)

F = (rho * ((Caudal/Area)**2) * Area_derivada / Area)

# Parámetros iniciales
xi = 0.0 # valor inicial de x
xf = 6.0 # valor final de x 
Pi = 340000.0  # valor inicial de la presion en Pascales
delta_x = 0.01
intervalo = (xf-xi) * delta_x # tamaño del paso
cantIntervalos = 1/delta_x
duracionGrafico = 10 #en segundos

plt.figure(figsize=(10, 6))
plt.xlabel('x')
plt.ylabel('P(x)')
plt.title('Presión en función de la distancia')
plt.grid(True)

metodoEulerRecursivo(f, xi, Pi, xf, intervalo)
plt.show()
