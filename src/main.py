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
    #plt.pause(5.0*delta_x)

    # Caso base
    if xi+intervalo >= xf : 
        return [[xi, yi]]
    
    #caso recursivo
    return [[xi, yi]]+ metodoEulerRecursivo(f, xi + intervalo , yi + intervalo * f(xi, yi) , xf, intervalo)
# Parámetros iniciales
xi = 0.0 # valor inicial de x
xf = 6.0 # valor final de x 
Pi = 340000.0  # valor inicial de la presion en Pascales
delta_x = 0.01 # 1-0.002
intervalo = (xf-xi) * delta_x # tamaño del paso


# Variables para almacenar datos y coordenadas
datos_calculados = []
coordenadas_ingresadas = []

def mostrar_datos():
    print("Se calcularon:", {len(datos_calculados)}, "valores de Presion")
    print("\n")
    for dato in datos_calculados:
        print(f"x: {dato[0]:.4f}, P: {dato[1]:.4f}")

def ingresar_coordenada():
    tiempo = float(input("Ingrese el tiempo: "))
    valor = float(input("Ingrese el valor de la imagen: "))
    plt.scatter(tiempo, valor, color='blue')
    plt.pause(0.01)
    coordenadas_ingresadas.append((tiempo, valor))
    # Búsqueda binaria y cálculo de error (pendiente)
    print(f"Coordenada ({tiempo}, {valor}) ingresada y graficada.")

def mostrar_historial():
    for coord in coordenadas_ingresadas:
        print(f"Tiempo: {coord[0]}, Valor: {coord[1]}")

def buscar_dato_por_tiempo():
    tiempo = float(input("Ingrese el tiempo: "))
    # Implementación de búsqueda de dato por tiempo (pendiente)
    print(f"Buscar dato en el tiempo {tiempo}.")

def buscar_dato_por_valor():
    valor = float(input("Ingrese el valor: "))
    # Implementación de búsqueda de dato por valor (pendiente)
    print(f"Buscar dato por el valor {valor}.")

def limpiar_consola():
    print("\033[H\033[J", end="")

def salir_programa():
    print("Saliendo del programa...")
    exit()

# Función principal del menú
def menu():
    while True:
        print("\n" + "="*40)
        print(" Paradigmas y Lenguajes de Programación I 📘")
        print("="*40)
        print("1. Mostrar los datos calculados 📊")
        print("2. Ingresar una coordenada para el cálculo de error 📍")
        print("3. Mostrar historial de coordenadas ingresadas 📝")
        print("4. Buscar un dato en la lista ingresando el tiempo 🔍")
        print("5. Buscar un dato en la lista ingresando el valor 🔎")
        print("6. Limpiar la consola 🧹")
        print("7. Salir del programa 🚪")
        print("="*40)

        match input("Seleccione una opción: "):
            case '1':
                mostrar_datos()
            case '2':
                ingresar_coordenada()
            case '3':
                mostrar_historial()
            case '4':
                buscar_dato_por_tiempo()
            case '5':
                buscar_dato_por_valor()
            case '6':
                limpiar_consola()
            case '7':
                salir_programa()
            case _:
                print("Opción no válida, por favor seleccione una opción del 1 al 7.")


if __name__ == "__main__":
    plt.figure(figsize=(10, 6))
    plt.xlabel('x')
    plt.ylabel('P(x)')
    plt.title('Presión en función de la distancia')
    plt.grid(True)

    F = F.evalf(subs={Y: Pi}) # evaluamos la constante de integracion con la Presion inicial

    datos_calculados = metodoEulerRecursivo(f, xi, Pi, xf, intervalo)
    #plt.show()

    menu()