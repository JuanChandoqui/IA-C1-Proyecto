from random import random
from matplotlib.colors import PowerNorm
from pandas import DataFrame, concat
from numpy import array_split
import random

def obtener_sectores(sudoku):
    sectores = []
    indice = 0
    while indice < 81:
        indiceSector = 0
        while indiceSector < 9:
            subsector = indice+indiceSector
            sectores.append(sudoku[subsector:subsector+3]+sudoku[subsector+9:subsector+12]+sudoku[subsector+18:subsector+21])
            indiceSector+=3
        indice+=27
    return sectores

def calcular_fitness(sudoku):
    filas = [sudoku[(i*9):(9*i)+9] for i in range(9)]
    columnas = [sudoku[i:81:9] for i in range(9)]
    sectores = obtener_sectores(sudoku)
    secciones = filas+columnas+sectores

    fitness = 0

    for seccion in secciones:
        numeros_repetidos= len(seccion) - len(set(seccion))
        if len(seccion) != len(set(seccion)):
            fitness+= numeros_repetidos

    return fitness

def cruza(poblacion):
    longitud_poblacion = len(poblacion['individuo'])
    indice_padres = array_split(random.sample(range(longitud_poblacion), longitud_poblacion),int(longitud_poblacion/2))
    descendientes = []
    for indice in indice_padres:
        padre1=poblacion['individuo'][indice[0]]
        padre2=poblacion['individuo'][indice[1]]

        numero_puntos = random.randint(1,9)
        puntos_cruza = list(reversed(sorted(random.sample(range(1, len(padre1)-1), numero_puntos))))
        hijo1 = []
        hijo2 = []
        cruza = False
        indice_punto = 0
        indice_maximo = len(padre1)
        while len(puntos_cruza) > 0:
            punto = puntos_cruza.pop()
            if cruza:
                hijo2+=padre1[indice_punto:punto]
                hijo1+=padre2[indice_punto:punto]
                cruza = False
            else:
                hijo1+=padre1[indice_punto:punto]
                hijo2+=padre2[indice_punto:punto]
                cruza = True
            indice_punto = punto
            if len(puntos_cruza) == 0:
                if cruza:
                    hijo2+=padre1[indice_punto:indice_maximo]
                    hijo1+=padre2[indice_punto:indice_maximo]
                    cruza = False
                else:
                    hijo1+=padre1[indice_punto:indice_maximo]
                    hijo2+=padre2[indice_punto:indice_maximo]
                    cruza = True
        descendientes.append(hijo1)
        descendientes.append(hijo2)
    return descendientes

def mutacion(descendientes,pmi,pmg):
    descendientes_mutados = []
    for individuo in descendientes:
        pmi_actual = random.uniform(0, 1)
        if pmi_actual <= pmi:
            for indice_gen in range(len(individuo)):
                pmg_actual=random.uniform(0, 1)
                if pmg_actual <= pmg:
                    individuo[indice_gen] = random.randint(1,9)
        descendientes_mutados.append(individuo)
    return descendientes_mutados

def poda(poblacion, poblacion_maxima):
    if len(poblacion.index) > poblacion_maxima:
        poblacion=poblacion.drop_duplicates(['genotipo'])
        if len(poblacion.index) > poblacion_maxima:
            poblacion = poblacion.iloc[0:poblacion_maxima]
    return poblacion.sort_values(by='fitness',ascending=True,ignore_index=True)


def imprime_sudoku(sudoku):
    x = 0
    y = 3

    iteracion = 0
    while iteracion < 9:
        if iteracion == 3 or iteracion == 6:
            print("----- + ----- + -----")

        for i in range(x, y):
            print(sudoku[i], end=" ")
        print("| ", end="")
        x += 3
        y += 3

        for i in range(x, y):
            print(sudoku[i], end=" ")
        print("| ", end="")
        x += 3
        y += 3

        for i in range(x, y):
            print(sudoku[i], end=" ")
        print()
        x += 3
        y += 3

        iteracion += 1

def main():
    poblacionInicial = 450
    longitudIndividuo = 81
    poblacion_maxima = 900

    individuos = [ [ random.randint(1, 9) for _ in range(longitudIndividuo)] for _ in range(poblacionInicial) ]

    # individuo = [5,3,4,6,7,8,9,1,2,6,7,2,1,9,5,3,4,8,1,9,8,3,4,2,5,6,7,8,5,9,7,6,1,4,2,3,4,2,6,8,5,3,7,9,1,7,1,3,9,2,4,8,5,6,9,6,1,5,3,7,2,8,4,2,8,7,4,1,9,6,3,5,3,4,5,2,8,6,1,7,9]
    # individuos.append(individuo)

    poblacion_data = {'individuo':individuos,'genotipo':[ ''.join(str(i)) for i in individuos],'fitness':map(calcular_fitness,individuos)}

    poblacion = DataFrame(poblacion_data).sort_values(by='fitness',ascending=True,ignore_index=True)
    numero_generaciones = 600
    generacion = 0
    while list(poblacion.iloc[0])[2] > 0 and generacion<numero_generaciones:
        print(f'{generacion}. mejor solucion: {list(poblacion.iloc[0])[2] }')
        descendientes = cruza(poblacion)
        nuevos_individuos = mutacion(descendientes,0.11,0.045)
        data_nuevos_individuos = {'individuo':nuevos_individuos,'genotipo':[ ''.join(str(i)) for i in nuevos_individuos],'fitness':map(calcular_fitness,nuevos_individuos)}
        pd_nuevos_individuos = DataFrame(data_nuevos_individuos)
        poblacion = concat([poblacion,pd_nuevos_individuos]).sort_values(by='fitness',ascending=True,ignore_index=True)
        poblacion = poda(poblacion,poblacion_maxima)
        generacion+=1
        # print(poblacion)
    if list(poblacion.iloc[0])[2] == 0:
        print(f'La solucion fue encontrada en la generación {generacion}')
        # print(list(poblacion.iloc[0])[0])
        return list(poblacion.iloc[0])[0]
    else:
        main()