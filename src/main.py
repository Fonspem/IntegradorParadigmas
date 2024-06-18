"""
Paradigmas y Lenguajes de Programación I
ok1.	Crear una función recursiva que aplique el método de Euler para resolver la ecuación diferencial planteada.
ok2.	Graficar en tiempo real la solución a medida que se calculan los valores recursivamente.
ok3.	Utilizar nodos y estructuras de datos (por ejemplo, listas enlazadas) para almacenar los datos calculados.
ok4.	Mostrar los datos almacenados en un formato legible.
ok5.	Implementar un menú interactivo con las siguientes opciones:
ok    a.	Mostrar los datos calculados.
ok    b.	Ingresar una coordenada para el cálculo de error:
ok        i.	Ingresar tiempo y valor de la imagen.
ok        ii.	Graficar el punto en la gráfica.
ok        iii.	Realizar una búsqueda binaria en la lista para calcular el error entre el punto ingresado y el punto correspondiente en el tiempo dado.??? mal planteada la consigna
ok    c.	Mostrar historial de coordenadas ingresadas y sus respectivos cálculos de error.
ok    d.	Buscar un dato en la lista ingresando el tiempo.
ok    e.	Buscar un dato en la lista ingresando la variable dependiente o su valor más cercano.
ok    f.	Limpiar la consola.
ok    g.	Salir del programa.
6.	Comparar la solución aproximada obtenida por el método de Euler (implementada en el programa) con la solución analítica.
7.	Analizar y explicar las diferencias observadas entre ambas soluciones.
ok8.	Añadir cualquier otra función que consideres necesaria para mejorar la eficiencia o funcionalidad del programa.
"""
import os
import time
from typing import Any, Optional
from numpy import block
from sympy import Symbol, diff, exp, pi, sqrt
import matplotlib.pyplot as plt

class Nodo:
    def __init__(self, data:Any):
        self._siguiente = None 
        self._dato = data

    @property
    def siguiente(self):
        return self._siguiente

    @siguiente.setter
    def siguiente(self, siguiente):
        self._siguiente = siguiente

    @property
    def dato(self)->Any:
        return self._dato

    @dato.setter
    def dato(self, data:Any):
        self._dato = data

class ListaEnlazada:
    def __init__(self):
        self._cabecera:None|Nodo = None
        self._cantidadDeNodos:int = 0
        self._recalcularCant:bool = False
        self._current_index = 0

    @property
    def cabecera(self):
        return self._cabecera

    @cabecera.setter
    def cabecera(self, valor:Any):
        self._cabecera = valor

    @property
    def cantidadDeNodos(self)->int: # recalcula la cantidad de nodos cada vez que se pida
        if self._recalcularCant:
            self._cantidadDeNodos = self.contarNodos()
            self._recalcularCant = False
        return self._cantidadDeNodos
    
    def contarNodos(self) -> int:
        contador:int = 0
        actual = self.cabecera
        while actual != None:
            actual = actual.siguiente
            contador += 1
        return contador

    def añadirAlFinal(self, nodo: Nodo):
        if self.cabecera:
            ultimoNodo = self.cabecera
            while ultimoNodo != None:
                if ultimoNodo.siguiente != None:
                    ultimoNodo = ultimoNodo.siguiente
                else:
                    ultimoNodo.siguiente = nodo
                    self._recalcularCant = True
                    break
        else:
            self._recalcularCant = True
            self.cabecera = nodo
        return self

    def añadirAlInicio(self, nodo: Nodo):
        nodo.siguiente = self.cabecera
        self.cabecera = nodo
        self._recalcularCant = True

    def eliminarNodo(self, nodo:Nodo):
        actual = self.cabecera
        previo = None
        while actual != None and actual != nodo:
            previo = actual
            actual = actual.siguiente
        if actual is None:
            self._recalcularCant = True
            return
        if previo is None:
            self.cabecera = actual.siguiente
        else:
            previo.siguiente = actual.siguiente
        actual.siguiente = None

    def mostrarTodosLosNodos(self):# muestra por consola
        temporal = self.cabecera
        print("Lista\n",end="->")
        while temporal != None:
            print(temporal.dato.presentacion(),end="\n->")
            temporal = temporal.siguiente
        print("--Null")
        print("\n")

    def listado(self)->list[Nodo]:# devuelve lista de nodos
        temporal = self.cabecera
        salida = list()
        while temporal != None:
            salida.append(temporal)
            temporal = temporal.siguiente
        return salida

    def __len__(self):
        return self.cantidadDeNodos
    
    def __add__(self, otra_lista):
        nueva_lista = ListaEnlazada()
        temporal = self.cabecera
        while temporal != None:
            nueva_lista.añadirAlFinal(Nodo(temporal.dato))
            temporal = temporal.siguiente
        temporal = otra_lista.cabecera
        while temporal != None:
            nueva_lista.añadirAlFinal(Nodo(temporal.dato))
            temporal = temporal.siguiente

        return nueva_lista
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._current_index < len(self.listado()):
            item = self.listado()[self._current_index]
            self._current_index += 1
            return item.dato
        else:
            self._current_index = 0
            raise StopIteration

X = Symbol("x") #Variable x de f
media = 3.0
desvioEst = 1

Area = (((1.5-((2/(desvioEst*sqrt(2*pi)))*exp(-((X-media)**2)/(2*desvioEst))))/2)**2)*pi

def A(x: float) :
    return Area.evalf(subs={X: x})

def A_derivada(x: float) -> float:
    return diff(Area, X).evalf(subs={X: x})

rho = 1000 # kg/m^3 1000:H2O, 1,2:aire
areaInicial = A(0.0) # m^2
velocidad = 1 #m/s
Caudal = areaInicial * velocidad #m^3/s

def V(x: float, Q: float) -> float: #retorna la velocidad del fuido en base al Area y el Caudal
    return (Q/A(x))

def f(x: float, p: float) -> float: #Funcion para Euler
    return rho * (V(x, Caudal)**2 * A_derivada(x)) / A(x)

Y = Symbol('y') # es para cargar el valor de la constante de integracion a la funcion
F = (- rho * ((Caudal/Area)**2) / 2) + Y + (rho * ((Caudal/Area)**2) / 2).evalf(subs={X: Y })


def metodoEulerRecursivo(f:float, xi:float, yi:float, xf:float, intervalo:float)-> ListaEnlazada:
    
    # Imprime los puntos calculados con Aproximacion de Euler
    plt.scatter(xi, yi , marker='o', color='red',s=30)
    
    # Imprime los puntos calculados resolviendo la ecuacion diferencial
    plt.scatter(xi, F.evalf(subs={X: xi}), color='blue',s=15)
    
    # Pausa para actualizar el gráfico
    plt.pause(5.0*delta_x)

    # Caso base
    if xi+intervalo >= xf :
        return ListaEnlazada().añadirAlFinal(Nodo([xi, yi]))
    
    #caso recursivo
    return ListaEnlazada().añadirAlFinal(Nodo([xi, yi])) + metodoEulerRecursivo(f, xi + intervalo , yi + intervalo * f(xi, yi) , xf, intervalo)

def metodoEulerLineal(f:float, xi:float, yi:float, xf:float, intervalo:float)-> ListaEnlazada:
    
    salida = ListaEnlazada()
    
    while xi+intervalo <= xf:
        
        # Imprime los puntos calculados con Aproximacion de Euler
        plt.scatter(xi, yi , marker='o', color='red',s=30)
        
        # Imprime los puntos calculados resolviendo la ecuacion diferencial
        plt.scatter(xi, F.evalf(subs={X: xi}), color='blue',s=15)
        
        # Pausa para actualizar el gráfico
        plt.pause(delta_x)
        
        
        salida.añadirAlFinal(Nodo([xi,yi]))
        
        xi += intervalo
        yi += intervalo * f(xi,yi)
        
    
    return salida


# Parámetros iniciales
xi = 0.0 # valor inicial de x
xf = 6.0 # valor final de x 
Pi = 20000.0  # valor inicial de la presion en Pascales
delta_x = 0.01 # 1-0.002
intervalo = (xf-xi) * delta_x # tamaño del paso

# Variables para almacenar datos y coordenadas
datosEuler = ListaEnlazada()
coordenadas = ListaEnlazada()
errorCoordenadas = ListaEnlazada()

def mostrar_datos():
    print("Se calcularon:", {len(datosEuler)-1}, "valores de presión.")
    print("\n")
    
    for datos in datosEuler:
        print(f"x: {datos[0]:.4f}, P: {datos[1]:.4f}")

def busquedaBinaria(lista:list, objetivo:Any) -> Optional[int]:
    izquierda:int = 0
    derecha:int = len(lista) - 1

    while izquierda <= derecha:
        medio:int = (izquierda + derecha) // 2
        valor_medio = lista[medio]

        if abs(valor_medio - objetivo) <= 0.001:
            return medio
        elif valor_medio < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return None

def distancia2D(x1:float,y1:float,x2:float,y2:float):
    return float(sqrt(((x1-x2)**2)+((y1-y2)**2)))

def valorMasCercano(valor:float, lista:list[float])-> float:
    mas_cercano = lista[0]
    for n in lista:
        if (n - valor)**2 < (mas_cercano - valor)**2:
            mas_cercano = n
    return mas_cercano

def puntoMasCercano(x1:float,y1:float, lista:ListaEnlazada)-> list[float,float]:
    mas_cercano = lista.cabecera.dato
    for n in lista:
        if distancia2D(x1,y1,n[0],n[1]) < distancia2D(x1,y1,mas_cercano[0],mas_cercano[1]):
            mas_cercano = n
    return mas_cercano

def ingresar_coordenada():
    while(True):
        try:
            distancia = float(input("Ingrese la distancia: "))
            presion = float(input("Ingrese el valor de la presión: "))
            if distancia < xi or distancia > xf:
                print("Distancia fuera de rango.")
                raise Exception
            if presion < 0:
                print("Presión fuera de rango.")
                raise Exception
            break
        except:
            print("Reintente el ingreso de datos")
    
    coordenadas.añadirAlFinal(Nodo([distancia, presion]))

    print(f"Coordenada (x={distancia}, P={presion}) ingresada.")


    dCerca,pCerca = puntoMasCercano(distancia,presion,datosEuler)
    
    print("La presión mas cercana que se ha precalculado es:", pCerca," Pa, en la posicion: ",dCerca," x.")
    print("La diferencia con el punto ingresado es:", pCerca-presion," Pa, ",dCerca-distancia," x.")
        
    errorCoordenadas.añadirAlFinal(Nodo([dCerca-distancia,pCerca-presion]))

    #imprime en grafico
    plt.scatter(distancia, presion, color='green',s=30,marker='s')
    plt.scatter(dCerca, pCerca, color='y',s=30,marker='s')
    plt.show(block=False)#no bloquea el programa


def mostrar_historial():
    print("Se ingresó:",len(coordenadas), "coordenada/s.")
    print("\n")
    for n in range(len(coordenadas)):
        coord = coordenadas.listado()[n].dato
        eCoord = errorCoordenadas.listado()[n].dato
        print(f"Distancia: {coord[0]:.4f}, Presión: {coord[1]:.4f}, De: {eCoord[0]:.4f}, Pe: {eCoord[1]:.4f}")

def buscar_dato_por_distancia():
    while(True):
        try:
            distancia = float(input("Ingrese posicion: "))
            if distancia < xi or distancia > xf:
                print("Fuera de rango.")
                raise Exception
            break
        except :
            print("Reintente el ingreso de datos.")
            
    print("Buscando presión para la distancia:", distancia)
    
    listaDeDistancias = list()
    
    for x in datosEuler:
        listaDeDistancias.append(x[0])
    
    mas_cercano = valorMasCercano(distancia, listaDeDistancias)

    indiceMasCercano = busquedaBinaria(listaDeDistancias,mas_cercano)
    print("La distancia precalculada mas cercana a ese valor es:", mas_cercano)
    print("con una presión de :",datosEuler.listado()[indiceMasCercano].dato[1])

def buscar_dato_por_presion():
    while(True):
        try:
            presion = float(input("Ingrese presión: "))
            if presion < 0:
                print("Fuera de rango.")
                raise Exception
            break
        except :
            print("Reintente el ingreso de datos.")

    print("Buscando la distancia calculada para la presión", presion)
    
    listaDePresiones = list()
    for x in datosEuler:
        listaDePresiones.append(x[1])

    indiceMasCercano = listaDePresiones.index(valorMasCercano(presion, listaDePresiones))
    
    print("La presión precalculada mas cercana a ese valor es:", datosEuler.listado()[indiceMasCercano].dato[1])
    print("en la distancia:",datosEuler.listado()[indiceMasCercano].dato[0])


# Función principal del menú
def menu():
    while True:
        print("\n" + "="*40)
        print(" Paradigmas y Lenguajes de Programación I 📘")
        print("="*40)
        print("1. Mostrar los datos calculados 📊")
        print("2. Ingresar una coordenada para el cálculo de error 📍")
        print("3. Mostrar historial de coordenadas ingresadas 📝")
        print("4. Buscar un dato en la lista ingresando la distancia 🔍")
        print("5. Buscar un dato en la lista ingresando el valor de la presión 🔎")
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
                buscar_dato_por_distancia()
            case '5':
                buscar_dato_por_presion()
            case '6':
                os.system('cls' if os.name == 'nt' else 'clear')
            case '7':
                print("Saliendo del programa...")
                exit()
            case _:
                print("Opción no válida, por favor seleccione una opción del 1 al 7.")

if __name__ == "__main__":
    
    plt.figure(figsize=(10, 6))
    plt.xlabel('x')
    plt.ylabel('P(x)')
    plt.title('Presión en función de la distancia')
    plt.grid(True)
    F = F.evalf(subs={Y: Pi}) # evaluamos la constante de integracion con la Presion inicial
    with plt.ion():
        plt.scatter(xi, 0, color='black',s=1,marker='s')
        plt.scatter(xf, Pi, color='black',s=1,marker='s')
        plt.show()
        datosEuler = metodoEulerLineal(f, xi, Pi, xf, intervalo)
        

    menu()