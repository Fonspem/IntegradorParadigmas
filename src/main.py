"""
Paradigmas y Lenguajes de Programación I
ok1.	Crear una función recursiva que aplique el método de Euler para resolver la ecuación diferencial planteada.
ok2.	Graficar en tiempo real la solución a medida que se calculan los valores recursivamente.
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
from sympy import Symbol, diff, exp, pi, sqrt
from typing import Tuple
import matplotlib.pyplot as plt

X = Symbol("x") #Variable x de f
media = 3.0
desvioEst = 0.6
DistNormal =  (exp(-0.5*((X-media)/desvioEst)**2)) / (sqrt(2 * pi) * desvioEst) 

Area = ( (2 - 2 * DistNormal))/2 * pi
  
def A(x: float) -> float:
    return Area.evalf(subs={X: x})

def A_derivada(x: float) -> float:
    return diff(Area, X).evalf(subs={X: x})

rho = 1000 # kg/m^3 1000:H2O, 1,2:aire
areaInicial = A(0.0) # m^2
velocidad = 3.0 #m/s
Caudal = areaInicial * velocidad #m^3/s

def V(x: float, Q: float) -> float: #retorna la velocidad del fuido en base al Area y el Caudal
    return (Q/A(x))

def f(x: float, p: float) -> float: #Funcion para Euler
    return rho * (V(x, Caudal)**2 * A_derivada(x)) / A(x)

Y = Symbol('y') # es para cargar el valor de la constante de integracion a la funcion
F = (- rho * ((Caudal/Area)**2) / 2) + Y + (rho * ((Caudal/Area)**2) / 2).evalf(subs={X: Y })

def metodoEulerRecursivo(f, xi:float, yi:float, xf:float, intervalo:float)-> list[list[float, float]]:
    
    # Imprime los puntos calculados resolviendo la ecuacion diferencial
    plt.scatter(xi, F.evalf(subs={X: xi}), color='blue',s=20)
    
    # Imprime los puntos calculados con Aproximacion de Euler
    plt.scatter(xi, yi , marker='o', color='r',s=20)
    
    # Pausa para actualizar el gráfico
    plt.pause(5.0*delta_x)

    # Caso base
    if xi >= xf: 
        return [xi, yi]
    
    #caso recursivo
    return [xi, yi] + metodoEulerRecursivo(f, xi + intervalo , yi + intervalo * f(xi, yi) , xf, intervalo)

# Parámetros iniciales
xi = 0.0 # valor inicial de x
xf = 6.0 # valor final de x 
Pi = 340000.0  # valor inicial de la presion en Pascales
delta_x = 0.01 # 1-0.002
intervalo = (xf-xi) * delta_x # tamaño del paso

F = F.evalf(subs={Y: Pi}) # evaluamos la constante de integracion con la Presion inicial


plt.figure(figsize=(10, 6))
plt.xlabel('x')
plt.ylabel('P(x)')
plt.title('Presión en función de la distancia')
plt.grid(True)

#estos puntos son para que se vea bien la escala del grafico, se puden cambiar sin problema
plt.scatter(xi, 290000.0 , marker='o', color='g',s=10)
plt.scatter(xf, Pi , marker='o', color='g',s=10)

metodoEulerRecursivo(f, xi, Pi, xf, intervalo)

plt.show()
