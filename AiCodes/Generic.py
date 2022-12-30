from time import time
from AlgorithmStarter import AlgorithmStart
from Sudoko import *
from SudokoFunc import *



class SudokuGA(object):
    _population_size = None
    _selection_rate = None
    _random_selection_rate = None
    _nb_children = None
    _max_nb_generations = None
    _mutation_rate = None
    _restart_after_n_generations_without_improvement = None
    _start_time = None

    def __init__(self,values ,population_size, selection_rate, random_selection_rate, nb_children, max_nb_generations,
                 mutation_rate, restart_after_n_generations_without_improvement):
      
        self._population_size = population_size
        self._selection_rate = selection_rate
        self._random_selection_rate = random_selection_rate
        self._nb_children = nb_children
        self._max_nb_generations = max_nb_generations
        self._mutation_rate = mutation_rate
        self._restart_after_n_generations_without_improvement = restart_after_n_generations_without_improvement
        self.values = values

    def run(self):

        #Start the Genetic algorithm to solve the objects
        values_to_set = self._load().get_initial_values()

        best_data = []
        worst_data = []
        found = False
        overall_nb_generations_done = 0
        restart_counter = 0

        while overall_nb_generations_done < self._max_nb_generations and not found:
            new_population = SudokoFunc.create_generation(self._population_size, values_to_set)

            nb_generations_done = 0
            remember_the_best = 0
            nb_generations_without_improvement = 0

            # Loop until max allowed generations is reached or a solution is found
            while nb_generations_done < self._max_nb_generations and not found:
                # Rank the solutions
                ranked_population = SudokoFunc.rank_population(new_population)
                best_solution = ranked_population[0]
                best_score = best_solution.fitness()
                worst_score = ranked_population[-1].fitness()
                best_data.append(best_score)
                worst_data.append(worst_score)

                # Manage best value and improvements among new generations over time
                if remember_the_best == best_score:
                    nb_generations_without_improvement += 1
                else:
                    remember_the_best = best_score
                if 0 < self._restart_after_n_generations_without_improvement < nb_generations_without_improvement:
                    print("No improvement since {} generations, restarting the program".format(self._restart_after_n_generations_without_improvement))

                    restart_counter += 1
                    break

                # Check if problem is solved and print best and worst results
                if best_score > 0:
                    print("Problem not solved on generation {} (restarted {} times). Best solution score is {} and ""worst is {}".format(nb_generations_done, restart_counter, best_score, worst_score))

                    # Not solved => select a new generation among this ranked population
                    # Retain only the percentage specified by selection rate
                    next_breeders = SudokoFunc.pick_from_population(ranked_population, self._selection_rate,
                                                                  self._random_selection_rate)

                    children = SudokoFunc.create_children_random_parents(next_breeders, self._nb_children)
                    new_population = SudokoFunc.mutate_population(children, self._mutation_rate)

                    nb_generations_done += 1
                    overall_nb_generations_done += 1
                else:
                    print("Problem solved after {} generations ({} overall generations)!!! Solution found is:".format(nb_generations_done, overall_nb_generations_done))     
                  #  best_solution.display()
                    self.values = best_solution.rows
                    found = True
                   # print("It took {} to solve it".format(tools.get_human_readable_time(self._start_time, time())))

        if not found:
            print("Problem not solved after {} generations. Printing best results below".format(overall_nb_generations_done))

            ranked_population = SudokoFunc.rank_population(new_population)
            best_solution = ranked_population[0]
            worst_solution = ranked_population[-1]
            #print("Best is:")
            #best_solution.display()
            self.values = best_solution.rows
            #print("Worst is:")
            #worst_solution.display()

        #graphics.draw_best_worst_fitness_scores(best_data, worst_data)

    def _load(self):

        if ((self._selection_rate + self._random_selection_rate) / 2) * self._nb_children != 1:
            raise Exception("Either the selection rate, random selection rate or the number of children is not "
                            "well adapted to fit the population")

        #values_to_set = fileloader.load_file_as_values(self._model_to_solve)
        values_to_set = self.values
        zeros_to_count = '0' if len(values_to_set) < 82 else '00'
       # print("The solution we have to solve is: (nb values to find = {})".format(values_to_set.count(zeros_to_count)))

        self._start_time = time()
        ss = Sudoko(values_to_set)
        #s.display()

        return ss

    def displays(self,val):

        for i in range(9):
            if i > 0 and i % 3 == 0:
                print("")
            # line = self.rows[i]
            for j in range(9):
                # val = line[j]
                if j > 0 and j % 3 == 0:
                    print('   {}'.format(val[(i * 9) + j]), end='')
                elif j == 8:
                    print(' {}'.format(val[(i * 9) + j]))
                else:
                    print(' {}'.format(val[(i * 9) + j]), end='')

        print("")

    def turn1d(self,val):
        answers = []
        for i in range(9):
            newVal = val[i]
            for j in range(9):
                answers.append(newVal[j])
        return answers



