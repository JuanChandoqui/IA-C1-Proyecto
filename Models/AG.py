from random import random
from pandas import DataFrame, concat
from numpy import array_split, mean
import random
import matplotlib.pyplot as plt

def evaluacion(poblacion):
    longitud_poblacion = len(poblacion['individuo'])
    padres = []
    indice_padres = array_split(random.sample(range(longitud_poblacion), longitud_poblacion),int(longitud_poblacion/2))
    for indice in indice_padres:
        individuo1=list(poblacion.iloc[indice[0]])
        individuo2=list(poblacion.iloc[indice[1]])
        if individuo1[2] > individuo2[2]:
            padres.append(indice[1])
        elif individuo2[2] > individuo1[2]:
            padres.append(indice[0])
        else:
            padres.append(indice[0])
            padres.append(indice[1])
    return array_split(padres,int(len(padres)/2))

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
    indice_padres=evaluacion(poblacion)
    descendientes = []
    for indice in indice_padres:
        if len(indice) == 2:
            padre1=poblacion['individuo'][indice[0]]
            padre2=poblacion['individuo'][indice[1]]

            numero_puntos = random.randint(1,len(padre1)-1)
            puntos_cruza = list(reversed(sorted(random.sample(range(1, len(padre1)), numero_puntos))))
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

def graficar(estadisticas):
    plt.plot(estadisticas['mejorCaso'], label="Mejor caso")
    plt.plot(estadisticas['promedio'],label="Caso promedio")
    plt.plot(estadisticas['peorCaso'], label="Peor Caso")
    plt.legend()
    plt.xlabel("Iteraciones")
    plt.ylabel("Aptitud")
    plt.title("EvolucionGeneraciones")
    plt.show()


def main():
    poblacionInicial = 30 #30 | 20
    poblacion_maxima = 200 #450 | 200

    estadisticas = {
        'mejorCaso':[],
        'peorCaso': [],
        'promedio': []
    }

    genotipo_individuos_iniciales = []
    individuos = []
    for _ in range(poblacionInicial):
        individuo = []
        for i in [random.sample(range(1,10), 9) for _ in range(9)]:
            individuo+=i
        individuos.append(individuo)
        genotipo_individuos_iniciales.append(''.join([ str(gen) for gen in individuo]))

    # individuo = [5,3,4,6,7,8,9,1,2,6,7,2,1,9,5,3,4,8,1,9,8,3,4,2,5,6,7,8,5,9,7,6,1,4,2,3,4,2,6,8,5,3,7,9,1,7,1,3,9,2,4,8,5,6,9,6,1,5,3,7,2,8,4,2,8,7,4,1,9,6,3,5,3,4,5,2,8,6,1,7,9]
    # individuos.append(individuo)

    poblacion_data = {'individuo':individuos,'genotipo': genotipo_individuos_iniciales,'fitness':map(calcular_fitness,individuos)}

    poblacion = DataFrame(poblacion_data).sort_values(by='fitness',ascending=True,ignore_index=True)

    numero_generaciones = 5000
    generacion = 0
    while list(poblacion.iloc[0])[2] > 0 and generacion<numero_generaciones:
        generacion+=1

        descendientes = cruza(poblacion)
        nuevos_individuos = mutacion(descendientes,0.85,0.029)
        genotipo_individuos_nuevos = []
        for genotipo in nuevos_individuos:
            genotipo_individuos_nuevos.append(''.join([ str(gen) for gen in genotipo]))

        data_nuevos_individuos = {'individuo':nuevos_individuos,'genotipo':genotipo_individuos_nuevos,'fitness':map(calcular_fitness,nuevos_individuos)}
        pd_nuevos_individuos = DataFrame(data_nuevos_individuos)
        poblacion = concat([poblacion,pd_nuevos_individuos]).sort_values(by='fitness',ascending=True,ignore_index=True)

        estadisticas['mejorCaso'].append(min(poblacion['fitness']))
        estadisticas['peorCaso'].append(max(poblacion['fitness']))
        estadisticas['promedio'].append(mean(poblacion['fitness']))

        poblacion = poda(poblacion,poblacion_maxima)
        print(f'{generacion}. mejor solucion: {list(poblacion.iloc[0])[2] }')

    if list(poblacion.iloc[0])[2] == 0:
        print(poblacion)
        print(f'La solucion fue encontrada en la generación {generacion-1}')
        print(list(poblacion.iloc[0])[0])
        graficar(estadisticas)
        return list(poblacion.iloc[0])[0]
    else:
        main()