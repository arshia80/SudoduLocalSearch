from random import randint
from math import sqrt
import numpy as np
#from Sudoko import positions, s_utils
import SudokoFunc
#from utils import tools


class Sudoko(object):

    grid_size = 0
    size = 0
    fixed_values = None
    rows = None
    columns = None
    grids_cell = None
    _fitness_score = None

    def __init__(self, values):

        #nb_rows = int(sqrt(len(values)))
        self.size = 9
        self.grid_size = 3
        self.rows = {}
        self.columns = {}
        self.grids_cell = {}
        self.fixed_values = {}
        self.init_values = []

        self.set_initial_values(values)

    def set_initial_values(self, values):

        self.init_values = values


        # Init the dicts
        for i in range(self.size):
            self.rows[i] = []
            self.columns[i] = []
            self.grids_cell[i] = []

        # In the above section we determine, according to the position in the given values, in which
        # column, row and grid the value belongs to
        position = 0
        for character in self.init_values:
            val = int(character)
            row_id = SudokoFunc.retrieve_row_id_from_position_and_size(position, self.size)
            col_id = SudokoFunc.retrieve_column_id_from_position_and_size(position, self.size)
            grid_id = SudokoFunc.retrieve_grid_id_from_row_and_col(row_id, col_id, self.grid_size)

            position += 1

            # Add this value to all dicts we maintain
            self.rows[row_id].append(val)
            self.columns[col_id].append(val)
            self.grids_cell[grid_id].append(val)

            # Keep knowledge of fixed values where key is their position (key= row_id|col_id)
            if val != 0:
                self.fixed_values[SudokoFunc.build_fixed_val_key(row_id, col_id)] = val
        return self

    def fill_random(self):

        #Randomly fill empty cells. Result is valid in terms of grids
        # Ensure that at least grids are 'correct' so we fill each one with available values to avoid duplicates
        for grid_id, grid_values in self.grids_cell.items():
            available_values = SudokoFunc.fill_with_some_valid_values(grid_values, self.size)

            # Get row and col from grid_id and position in grid and substitute the value
            for position, new_value in enumerate(available_values):
                row_id = SudokoFunc.retrieve_row_id_from_grid_id_and_position(grid_id, position, self.grid_size)
                col_id = SudokoFunc.retrieve_column_id_from_grid_id_and_position(grid_id, position, self.grid_size)
                self.columns[col_id][row_id] = new_value
                self.rows[row_id][col_id] = new_value

            # Substitute value with new one in grids arrays
            self.grids_cell[grid_id] = available_values
        return self

    def fill_with_grids(self, grids):

        for grid_id, grid_values in enumerate(grids):
            # Get row and col from grid_id and position in grid and substitute the value
            for position, value in enumerate(grid_values):
                row_id = SudokoFunc.retrieve_row_id_from_grid_id_and_position(grid_id, position, self.grid_size)
                col_id = SudokoFunc.retrieve_column_id_from_grid_id_and_position(grid_id, position, self.grid_size)
                self.columns[col_id][row_id] = value
                self.rows[row_id][col_id] = value

                self.grids_cell[grid_id][position] = value
        return self



    def grids(self):
        return self.grids_cell

    def rows(self):
        return self.rows

    def columns(self):
        return self.columns

    def size(self):
        return self.size

    def grid_size(self):
        return self.grid_size

    def get_initial_values(self):
        return self.init_values

    def fitness(self):

        #this show how many figures are at the right place among the number of figures to find
        # Evaluate once per individual
        if self._fitness_score is None:
            duplicates_counter = 0
            for i in range(self.size):
                duplicates_counter += SudokoFunc.count_duplicates(self.rows[i]) + SudokoFunc.count_duplicates(self.columns[i])
            self._fitness_score = duplicates_counter
        return self._fitness_score

    def swap_2_values(self):

        #Pick randomly 2 elements to swap if they are not fixed values
        # Pick a random grid
        grid_id = np.random.randint(0, self.size - 1)

        rand_pos_1, row_id_1, col_id_1 = self.get_random_not_fixed(grid_id, -1)
        rand_pos_2, row_id_2, col_id_2 = self.get_random_not_fixed(grid_id, rand_pos_1)

        grid_values = self.grids_cell[grid_id]
        val_1 = grid_values[rand_pos_1]
        val_2 = grid_values[rand_pos_2]

        grid_values[rand_pos_1] = val_2
        grid_values[rand_pos_2] = val_1
        self.rows[row_id_1][col_id_1] = val_2
        self.rows[row_id_2][col_id_2] = val_1
        self.columns[col_id_1][row_id_1] = val_2
        self.columns[col_id_2][row_id_2] = val_1

        return self

    def is_fixed(self, row_id, col_id):
        return SudokoFunc.build_fixed_val_key(row_id, col_id) in self.fixed_values

    def get_random_not_fixed(self, grid_id, forbidden_pos):
        rand_pos = -1
        row_id = -1
        col_id = -1
        is_fixed = True
        while is_fixed or rand_pos == forbidden_pos:
            rand_pos = randint(0, self.size - 1)
            # We need to find their position (row and column) in the whole table to check whether it is fixed or not
            row_id = SudokoFunc.retrieve_row_id_from_grid_id_and_position(grid_id, rand_pos, self.grid_size)
            col_id = SudokoFunc.retrieve_column_id_from_grid_id_and_position(grid_id, rand_pos, self.grid_size)
            is_fixed = self.is_fixed(row_id, col_id)
        return rand_pos, row_id, col_id



























