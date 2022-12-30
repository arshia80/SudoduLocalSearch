

from random import shuffle
import numpy as np
import random
from Sudoko import *

def build_fixed_val_key(row_id, col_id):
    return "[{}|{}]".format(str(row_id), str(col_id))





def retrieve_row_id_from_position_and_size(position, size):
    return position // size

def retrieve_column_id_from_position_and_size(position, size):
    return position % size


def retrieve_grid_id_from_row_and_col(row_id, col_id, grid_size):
    return int(col_id // grid_size + ((row_id // grid_size) * grid_size))


def retrieve_range_rows_from_grid_id(grid_id, grid_size):
    start = int(grid_id / grid_size) * grid_size
    return range(start, start + grid_size)


def retrieve_range_columns_from_grid_id(grid_id, grid_size):
    start = int(grid_id % grid_size) * grid_size
    return range(start, start + grid_size)


def retrieve_row_id_from_grid_id_and_position(grid_id, grid_position, grid_size):
    row_in_grid = retrieve_row_id_from_position_and_size(grid_position, grid_size)
    delta_row = grid_size * (retrieve_row_id_from_position_and_size(grid_id, grid_size))
    return delta_row + row_in_grid


def retrieve_column_id_from_grid_id_and_position(grid_id, grid_position, grid_size):

    col_in_grid = retrieve_column_id_from_position_and_size(grid_position, grid_size)
    delta_col = grid_size * (retrieve_column_id_from_position_and_size(grid_id, grid_size))
    return delta_col + col_in_grid


def fill_with_some_valid_values(array_to_fill, length):

    # Get fixed values
    fixed_values = [value for value in array_to_fill if value > 0]
    # Get fixed values and their index
    fixed_index_values = [(pos, value) for pos, value in enumerate(array_to_fill) if value > 0]
    # Determine what are the available values based on fixed values
    available_values = [x for x in range(1, length + 1) if x not in fixed_values]
    shuffle(available_values)
    # Add fixed values in the shuffled array
    for index, val in fixed_index_values:
        available_values.insert(index, val)
    return available_values



def count_duplicates(arr):
    #Count how many times the same value is found in a given array
    # Size of the given array minus the size of unique elements found in this array = nb of duplicates
    return len(arr) - len(set(arr))



#sag

def create_generation(population_size, values_to_set):

   # Create the first generation knowing its size

    population = []
    for i in range(population_size):
        population.append(Sudoko(values_to_set).fill_random())
    return population


def rank_population(population):

    individuals_and_score = {}
    for individual in population:
        individuals_and_score[individual] = individual.fitness()
    return sorted(individuals_and_score, key=individuals_and_score.get)


def pick_from_population(ranked_population, selection_rate, random_selection_rate):

    next_breeders = []

    nb_best_to_select = int(len(ranked_population) * selection_rate)
    nb_random_to_select = int(len(ranked_population) * random_selection_rate)

    # Keep n best elements in the population + randomly n other elements (note: might be the same)
    for i in range(nb_best_to_select):
        next_breeders.append(ranked_population[i])
    for i in range(nb_random_to_select):
        next_breeders.append(random.choice(ranked_population))

    # Shuffle everything to avoid having only the best (copyright Tina Turner) at the beginning
    np.random.shuffle(next_breeders)
    return next_breeders




def create_children_random_parents(next_breeders, nb_children):

    next_population = []
    # Randomly pick 1 father and 1 mother until new population is filled
    range_val = int(len(next_breeders)/2) * nb_children
    for _ in range(range_val):
        father = random.choice(next_breeders)
        mother = random.choice(next_breeders)
        next_population.append(create_one_child_random_elements(father, mother, father.get_initial_values()))
    return next_population



def create_one_child_random_elements(father, mother, values_to_set):

    sudoku_size = father.size
    elements_from_mother = np.random.randint(0, sudoku_size, np.random.randint(1, sudoku_size - 1))

    child_grids = []
    for i in range(sudoku_size):
        if i in elements_from_mother:
            child_grids.append(mother.grids()[i])
        else:
            child_grids.append(father.grids()[i])
    return Sudoko(values_to_set).fill_with_grids(child_grids)


def mutate_population(population, mutation_rate):

    population_with_mutation = []
    for individual in population:
        if np.random.random() < mutation_rate:
            individual = individual.swap_2_values()
        population_with_mutation.append(individual)
    return population_with_mutation