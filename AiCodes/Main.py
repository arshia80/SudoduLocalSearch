import argparse
from ast import literal_eval
import json
from Generic import *







if __name__ == '__main__':


    jsonStr = ' {"sudoku":[[0, 8, 0, 0, 0, 0, 0, 9, 0], [0, 0, 7, 5, 0, 2, 8, 0, 0], [6, 0, 0, 8, 0, 7, 0, 0, 5],[3, 7, 0, 0, 8, 0, 0, 5, 1], [2, 0, 0, 0, 0, 0, 0, 0, 8], [9, 5, 0, 0, 4, 0, 0, 3, 2],[8, 0, 0, 1, 0, 4, 0, 0, 9], [0, 0, 1, 9, 0, 3, 6, 0, 0], [0, 4, 0, 0, 0, 0, 0, 2, 0]] }'


    values2 = [[0, 8, 0, 0, 0, 0, 0, 9, 0], [0, 0, 7, 5, 0, 2, 8, 0, 0], [6, 0, 0, 8, 0, 7, 0, 0, 5],
              [3, 7, 0, 0, 8, 0, 0, 5, 1], [2, 0, 0, 0, 0, 0, 0, 0, 8], [9, 5, 0, 0, 4, 0, 0, 3, 2],
              [8, 0, 0, 1, 0, 4, 0, 0, 9], [0, 0, 1, 9, 0, 3, 6, 0, 0], [0, 4, 0, 0, 0, 0, 0, 2, 0]]

    values1 = [[0, 0, 0, 0, 0, 0, 6, 8, 0], [0, 0, 0, 0, 7, 3, 0, 0, 9], [3, 0, 9, 0, 0, 0, 0, 4, 5],
              [4, 9, 0, 0, 0, 0, 0, 0, 0], [8, 0, 3, 0, 5, 0, 9, 0, 2], [0, 0, 0, 0, 0, 0, 0, 3, 6],
              [9, 6, 0, 0, 0, 0, 3, 0, 8], [7, 0, 0, 6, 8, 0, 0, 0, 0], [0, 2, 8, 0, 0, 0, 0, 0, 0]]

    values = [[0, 3, 0, 0, 7, 0, 0, 5, 0], [5, 0, 0, 1, 0, 6, 0, 0, 9], [0, 0, 1, 0, 0, 0, 4, 0, 0],
              [0, 9, 0, 0, 5, 0, 0, 6, 0], [6, 0, 0, 4, 0, 2, 0, 0, 7], [0, 4, 0, 0, 1, 0, 0, 3, 0],
              [0, 0, 2, 0, 0, 0, 8, 0, 0], [9, 0, 0, 3, 0, 5, 0, 0, 2], [0, 1, 0, 0, 2, 0, 0, 7, 0]]

    population_size = 10000
    selection_rate = 0.45
    random_selection_rate = 0.05
    nb_children = 4
    max_nb_generations = 1000
    mutation_rate = 0.06

    restart_after_n_generations_without_improvement = 40

    y = json.loads(jsonStr)
    z = y['sudoku']

    new_values = []
    for i in range(9):
        for j in range(9):
            new_values.append(z[i][j])

    sga = SudokuGA(new_values,population_size, selection_rate, random_selection_rate, nb_children, max_nb_generations,mutation_rate, restart_after_n_generations_without_improvement)

    sga.displays(sga.values) #display not complete sudoku
    sga.run()
    sga.values = sga.turn1d(sga.values)
    sga.displays(sga.values)#display  complete sudoku


    finalValues = [[0 for x in range(9)] for y in range(9)]
    for i in range(9):
        for j in range(9):
           finalValues[i][j] = sga.values[(i*9) + j]

    y['sudoku'] = finalValues
    final_json_str = json.dumps(y)

    print(final_json_str)