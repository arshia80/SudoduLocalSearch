from ai import AI

if __name__ == '__main__':

    ai = AI()
    jsonStr = ' {"sudoku":[[0, 8, 0, 0, 0, 0, 0, 9, 0], [0, 0, 7, 5, 0, 2, 8, 0, 0], [6, 0, 0, 8, 0, 7, 0, 0, 5],[3, 7, 0, 0, 8, 0, 0, 5, 1], [2, 0, 0, 0, 0, 0, 0, 0, 8], [9, 5, 0, 0, 4, 0, 0, 3, 2],[8, 0, 0, 1, 0, 4, 0, 0, 9], [0, 0, 1, 9, 0, 3, 6, 0, 0], [0, 4, 0, 0, 0, 0, 0, 2, 0]] }'
    returnd_json = ai.solve(jsonStr)
    print(returnd_json)