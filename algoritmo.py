import heapq
import numpy as np

class Mapa:
    def __init__(self, tablero, meta, padre=None, movimiento=0, profundidad=0) -> None:
        self.tablero = tablero
        self.padre = padre
        self.movimiento = movimiento
        self.profundidad = profundidad
        if padre:
            self.costo = padre.costo + 1
        else:
            self.costo = 0
        self.heuristica = self.calcular_distancia(meta)
        self.evaluacion = self.costo + self.heuristica
        print(f'Se inicializó un mapa con la matriz:\n{self.tablero}\nCosto: {self.costo}, Heurística: {self.heuristica}, Evaluación: {self.evaluacion}')

    def calcular_distancia(self, meta):
        distancia = 0
        for num in range(1, 9):
            pos = np.where(self.tablero == num)
            meta_pos = np.where(meta == num)
            distancia += abs(pos[0] - meta_pos[0]) + abs(pos[1] - meta_pos[1])
        print(f'Distancia calculada: {distancia}')
        return distancia

    def generar_sucesores(self, meta):
        sucesores = []
        fila, columna = np.where(self.tablero == 0)
        fila, columna = fila[0], columna[0]
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in direcciones:
            nueva_fila, nueva_columna = fila + dr, columna + dc
            if 0 <= nueva_fila < 3 and 0 <= nueva_columna < 3:
                nuevo_tablero = self.tablero.copy()
                nuevo_tablero[fila, columna], nuevo_tablero[nueva_fila, nueva_columna] = (
                    nuevo_tablero[nueva_fila, nueva_columna],
                    nuevo_tablero[fila, columna],
                )
                sucesores.append(
                    Mapa(nuevo_tablero, meta, self, self.movimiento + 1, self.profundidad + 1)
                )
        print(f'Se generaron {len(sucesores)} sucesores')
        return sucesores

    def __lt__(self, other):
        return self.evaluacion < other.evaluacion


class Solucionador:
    def __init__(self, inicio, meta) -> None:
        self.inicio = inicio
        self.meta = meta
        print(f'Se inicializó el solucionador con inicio:\n{self.inicio}\nMeta:\n{self.meta}')

    def resolver(self):
        lista_abierta = []
        heapq.heappush(lista_abierta, Mapa(self.inicio, self.meta))
        conjunto_cerrado = set()

        while lista_abierta:
            actual = heapq.heappop(lista_abierta)
            print(f'Se sacó el mapa con la matriz:\n{actual.tablero}\nDe la lista abierta')
            if np.array_equal(actual.tablero, self.meta):
                print('¡Meta alcanzada!')
                return actual

            conjunto_cerrado.add(tuple(actual.tablero.flatten()))
            for sucesor in actual.generar_sucesores(self.meta):
                if tuple(sucesor.tablero.flatten()) not in conjunto_cerrado:
                    heapq.heappush(lista_abierta, sucesor)
                    print(f'Se agregó el mapa con la matriz:\n{sucesor.tablero}\nA la lista abierta')

        print('No se encontró solución')
        return None

    def imprimir_solucion(self, solucion):
        camino = []
        while solucion:
            camino.append(solucion.tablero)
            solucion = solucion.padre
        for estado in reversed(camino):
            print(estado)
            print()


inicio = np.array([[1, 2, 3], [5, 6, 0], [7, 8, 4]])
meta = np.array([[1, 2, 3], [5, 8, 6], [0, 7, 4]])
solucionador = Solucionador(inicio, meta)
solucion = solucionador.resolver()
if solucion:
    print("La forma de solucionarlo es:")
    solucionador.imprimir_solucion(solucion)
else:
    print("No se encontró solución")