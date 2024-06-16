import math
import time
from typing import List, Tuple
import matplotlib.pyplot as plt

Tiempo_a_demorar = 10

def metodoEulerRecursivo(f, xi: float, yi: float, xf: float, intervalo: float) -> List[Tuple[float, float]]:
    plt.plot([xi, xi + intervalo], [yi, yi + intervalo * f(xi, yi)], marker='o', linestyle='-', color='r')
    plt.pause(Tiempo_a_demorar / cantIntervalos)  # Pausa para actualizar el gráfico
    if xi >= xf:
        return [(xi, yi)]
    return [(xi, yi)] + metodoEulerRecursivo(f, xi + intervalo, yi + intervalo * f(xi, yi), xf, intervalo)

rho = 1000  # kg/m^3 1000:H2O, 1,2:aire
areaInicial = 3.1415 * (0.03 / 2)**2  # m^2
areaFinal = 3.1415 * (0.05 / 2)**2  # m^2
velocidad = 3.0  # m/s
Caudal = areaInicial * velocidad  # m^3/s

def f(x: float, p: float) -> float:
    return rho * (V(x, Caudal)**2 * A_derivada(x)) / A(x)

def V(x: float, Q: float) -> float:
    return (Q / A(x))

def A(x: float) -> float:
    if x <= areaInicial:
        return areaInicial
    elif x > areaInicial and x <= areaFinal:
        return x
    elif x > areaFinal:
        return areaFinal

def A_derivada(x: float) -> float:
    if x <= areaInicial:
        return 0
    elif x > areaInicial and x <= areaFinal:
        return 1
    elif x > areaFinal:
        return 0

# Parámetros iniciales
xi = 0.0  # valor inicial de x
xf = 2 * areaInicial + areaFinal  # valor final de x 
Pi = 340000.0  # valor inicial de la presión
delta_x = 0.05
intervalo = areaInicial * delta_x  # tamaño del paso
cantIntervalos = (xf - xi) / intervalo

# Variables para almacenar datos y coordenadas
datos_calculados = []
coordenadas_ingresadas = []

def mostrar_datos():
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

#mostrar el menú
def mostrar_menu():
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

# Función principal del menú
def menu():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            mostrar_datos()
        elif opcion == '2':
            ingresar_coordenada()
        elif opcion == '3':
            mostrar_historial()
        elif opcion == '4':
            buscar_dato_por_tiempo()
        elif opcion == '5':
            buscar_dato_por_valor()
        elif opcion == '6':
            limpiar_consola()
        elif opcion == '7':
            salir_programa()
        else:
            print("Opción no válida, por favor seleccione una opción del 1 al 7.")

if __name__ == "__main__":
    plt.figure(figsize=(10, 6))
    plt.xlabel('x')
    plt.ylabel('P(x)')
    plt.title('Presión en función de la distancia')
    plt.grid(True)

    datos_calculados = metodoEulerRecursivo(f, xi, Pi, xf, intervalo)
    plt.show()

    menu()
