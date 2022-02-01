import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools

sudokuResuelto = []

def calcula_fitness(sudoku):
    def repetidos(aux):
        fit = 0
        if len(aux) != len(set(aux)):
            fit = len(aux) - len(set(aux))
        return fit

    def evalua_filas_o_columnas(sudoku, fil_col, desplazamiento):
        iteracion = 0
        fit = 0
        while iteracion < 9:
            aux = list()

            for i in fil_col:
                aux.append(sudoku[i])

            fit += repetidos(aux)

            for i in range(0, len(fil_col)):
                fil_col[i] += desplazamiento

            iteracion += 1
        return fit

    fitness  = 0
    columnas = [0, 9, 18, 27, 36, 45, 54, 63, 72]
    filas    = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    # Evalúa las columnas
    fitness += evalua_filas_o_columnas(sudoku, columnas, 1)

    # Evalúa las filas
    fitness += evalua_filas_o_columnas(sudoku, filas, 9)

    # Evalúa los sectores
    posiciones_sectores = [0, 3, 6, 27, 30, 33, 54, 57, 60]
    for i in posiciones_sectores:
        aux = recorre_sectores(sudoku, i)
        fitness += repetidos(aux)

    return (float(fitness),)

def recorre_sectores(sudoku, posicion):
        sector = [
            sudoku[posicion+0+0],  sudoku[posicion+1+0],  sudoku[posicion+2+0],
            sudoku[posicion+0+9],  sudoku[posicion+1+9],  sudoku[posicion+2+9],
            sudoku[posicion+0+18], sudoku[posicion+1+18], sudoku[posicion+2+18]
        ]
        return sector

def repetidos(aux):
    fit = 0
    if len(aux) != len(set(aux)):
        fit = len(aux) - len(set(aux))
    return fit

def evalua_filas_o_columnas(sudoku, fil_col, desplazamiento):
        iteracion = 0
        fit = 0
        while iteracion < 9:
            aux = list()

            for i in fil_col:
                aux.append(sudoku[i])

            fit += repetidos(aux)

            for i in range(0, len(fil_col)):
                fil_col[i] += desplazamiento

            iteracion += 1
        return fit

def recorre_sectores(sudoku, posicion):
        sector = [
            sudoku[posicion+0+0],  sudoku[posicion+1+0],  sudoku[posicion+2+0],
            sudoku[posicion+0+9],  sudoku[posicion+1+9],  sudoku[posicion+2+9],
            sudoku[posicion+0+18], sudoku[posicion+1+18], sudoku[posicion+2+18]
        ]
        return sector

def get_sudoku():
    return sudokuResuelto

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

def shuffle_in_place(genes, first, last):
    while first < last:
        index = random.randint(first, last)
        genes[first], genes[index] = genes[index], genes[first]
        first += 1

def index_row(index):
    return int(index / 9)

def index_column(index):
    return int(index % 9)

def row_column_section(row, column):
    return int(row / 3) * 3 + int(column / 3)

def section_start(index):
    return int((index_row(index) % 9) / 3) * 27 + int(
        index_column(index) / 3) * 3

def build_validation_rules():
    rules = []
    for index in range(80):
        itsRow = index_row(index)
        itsColumn = index_column(index)
        itsSection = row_column_section(itsRow, itsColumn)

        for index2 in range(index + 1, 81):
            otherRow = index_row(index2)
            otherColumn = index_column(index2)
            otherSection = row_column_section(otherRow, otherColumn)
            if itsRow == otherRow or \
                            itsColumn == otherColumn or \
                            itsSection == otherSection:
                rules.append(Rule(index, index2))

    rules.sort(key=lambda x: x.OtherIndex * 100 + x.Index)
    return rules

class Rule:
    def __init__(self, it, other):
        if it > other:
            it, other = other, it
        self.Index = it
        self.OtherIndex = other

    def __eq__(self, other):
        return self.Index == other.Index and \
               self.OtherIndex == other.OtherIndex

    def __hash__(self):
        return self.Index * 100 + self.OtherIndex

validationRules = build_validation_rules()

def mutate(genes, validationRules):
    selectedRule = next(rule for rule in validationRules
                        if genes[rule.Index] == genes[rule.OtherIndex])
        
    if selectedRule is None:
        return

    if index_row(selectedRule.OtherIndex) % 3 == 2 \
            and random.randint(0, 10) == 0:
        sectionStart = section_start(selectedRule.Index)
        current = selectedRule.OtherIndex
        while selectedRule.OtherIndex == current:
            shuffle_in_place(genes, sectionStart, 80)
            selectedRule = next(rule for rule in validationRules
                                if genes[rule.Index] == genes[rule.OtherIndex])
        return

    row = index_row(selectedRule.OtherIndex)
    start = row * 9
    indexA = selectedRule.OtherIndex
    indexB = random.randrange(start, len(genes))
    genes[indexA], genes[indexB] = genes[indexB], genes[indexA]

def dinamica_evolutiva(estadisticas):
    def add_estadisticas(poblacion, iteracion=1):
        fitnesses = [individual.fitness.values[0] for individual in poblacion]
        return {
            "ite" :  iteracion,
            "mean":  np.mean(fitnesses),
            "std" :  np.std(fitnesses),
            "max" :  np.max(fitnesses),
            "min" :  np.min(fitnesses)
        }

    pop = toolbox.population(n=500)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.83, 0.75

    print("Start of evolution")

    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    fits = [ind.fitness.values[0] for ind in pop]
    g = 0

    while min(fits) > 0 and g < 200:
        g = g + 1
        print("-- Generación %i --" % g)

        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                mutate(mutant, validationRules)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # print("  Evaluated %i individuals" % len(invalid_ind))

        pop[:] = offspring
        
        estadisticas.append(add_estadisticas(pop, g))
        
        fits = [ind.fitness.values[0] for ind in pop]
        
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        # print("  Min %s" % min(fits))
        # print("  Max %s" % max(fits))
        # print("  Avg %s" % mean)
        # print("  Std %s" % std)

    best_ind = tools.selBest(pop, 1)[0]

    return {
        "best_ind" :  best_ind,
        "g"        :  g
    }

def main(estadisticas):
    global sudokuResuelto
    try:
        resultado = dinamica_evolutiva(estadisticas)
        if resultado["best_ind"].fitness.values[0] != 0.0:
            main(estadisticas)
        else:
            print("\n\nSOLUCIÓN en la generación {}".format(resultado["g"]))
            imprime_sudoku(resultado["best_ind"])
            sudokuResuelto = resultado["best_ind"]
            print("Fitness: {}".format(resultado["best_ind"].fitness.values[0]))
            
    except:
        main(estadisticas)

def grafica(estadisticas):
    plt.scatter(range(1, len(estadisticas)+1), [s["min"] for s in estadisticas], marker=".")
    plt.title("Promedio de fitness por iteración")
    plt.xlabel("Iteraciones")
    plt.ylabel("Fitness")
    plt.show()

def inicializar():
    estadisticas = list()
    main(estadisticas)
    
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))    # Se crea la clase "FitnessMin", derivada de la clase "base.Fitness"
creator.create("Individual", list, fitness=creator.FitnessMin) # Se crea la clase Individual, representada en el tipo de dato "lista"

# Se instancia el objeto toolbox de la clase "base.Toolbox()". Este objeto contiene el método "register" que se usará a continuación
toolbox = base.Toolbox()

# Se registra la función fitness
toolbox.register("evaluate", calcula_fitness)

TAMANIO_INDIVIDUO = 81 # Tamaño de cada individuo (sudokus aleatorios generados)

# "toolbox.register"() añade un método al objeto "toolbox". Este método es denominado "entero_aleatorio" y llama a la función...
#  "random.randint" generando un número aleatorio entre 1 y 9 (los valores válidos del sudoku)
toolbox.register("entero_aleatorio", random.randint, 1, 9)

# Este método genera un nuevo individuo
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.entero_aleatorio, n=TAMANIO_INDIVIDUO)

# Este método genera una nueva población, llamando al método que genera individuos
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Operador de cruce. Registra el método para el cruce en 2 puntos
toolbox.register("mate", tools.cxTwoPoint)

# Operador de Selección. El método de selección es por "torneo", tomando como criterio de selección el fitness
toolbox.register("select", tools.selTournament, tournsize=3, fit_attr="fitness")

# grafica(estadisticas)