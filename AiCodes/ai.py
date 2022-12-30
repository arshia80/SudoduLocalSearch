import json
from Generic import *

# *** you can change everything except the name of the class, the act function and the problem_data ***

class AI:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self):
        pass

    # the solve function takes a json string as input
    # and outputs the solved version as json
    def solve(self, problem):
        # ^^^ DO NOT change the solve function above ***

        problem_data = json.loads(problem)
        # ^^^ DO NOT change the problem_data above ***


        # TODO implement your code here

        population_size = 10000
        selection_rate = 0.45
        random_selection_rate = 0.05
        nb_children = 4
        max_nb_generations = 1000
        mutation_rate = 0.06
        presolving = False
        restart_after_n_generations_without_improvement = 40

        z = problem_data['sudoku']

        #turn our data to 1d
        new_values = []
        for i in range(9):
            for j in range(9):
                new_values.append(z[i][j])

        sga = SudokuGA(new_values, population_size, selection_rate, random_selection_rate, nb_children,max_nb_generations, mutation_rate, restart_after_n_generations_without_improvement)
        sga.displays(sga.values)
        sga.run()
        sga.values = sga.turn1d(sga.values)
        sga.displays(sga.values)

        finalValues = [[0 for x in range(9)] for y in range(9)]
        for i in range(9):
            for j in range(9):
                finalValues[i][j] = sga.values[(i * 9) + j]

        problem_data['sudoku'] = finalValues
        finished = json.dumps(problem_data)

        # finished is the solved version
        return finished
