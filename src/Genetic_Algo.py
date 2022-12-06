import copy
import operator

import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt


class Genetic:
    """
    A Genetic Algorithm class
    """

    def __init__(self, buildings=None, residences=None) -> None:
        """
        The following are performed in this __init__ function
        - Initialize the genetic algorithm class
        - reads in timetable data
        - Encodes courses to integers ranging from [0,37]
        - Initialize a population
        """

        data = pd.read_csv("data/students.csv")[["mandatory_1", "mandatory_2",
                                                 "mandatory_3", "elective_1",
                                                 "elective_2"]]
        self.data = np.array(data).tolist()
        self.residence_a, self.residence_b, self.residence_c = self.data[:10], self.data[10:20], self.data[20:]

        info_ = []
        for i in data.columns:
            info_.extend(data[i].unique().tolist())
        self.info = dict(list(zip(range(40), list(sorted(set(info_))))))
        self.encoding = {value: key for key, value in self.info.items()}
        self.bounds = {"A": 2, "B": 3, "C": 3, "D": 2}
        self.chromosome = list(range(38)) + [0, 1]
        self.buildings = buildings
        self.residences = residences
        self.population = []
        self.distances = {"residence_a": {"A": 6, "B": 7, "C": 8, "D": 9},
                          "residence_b": {"A": 7, "B": 7, "C": 6, "D": 7},
                          "residence_c": {"A": 9, "B": 9, "C": 7, "D": 7},
                          "A": {"A": 0, "B": 1, "C": 2, "D": 3},
                          "B": {"A": 1, "B": 0, "C": 2, "D": 3},
                          "C": {"A": 2, "B": 2, "C": 0, "D": 1},
                          "D": {"A": 3, "B": 3, "C": 1, "D": 0}}
        self.pop_size = 100
        self.n_keep = 5
        self.n_reproduce = self.pop_size // self.n_keep

        np.random.seed(42)
        for i in range(self.pop_size):
            self.population.append(np.random.permutation(self.chromosome).tolist())

    def fitness(self, pop: list) -> int:
        """
        returns the total fitness of the gene pool
        :param pop: gene pool (population)
        :return: fitness value of the gene pool
        """
        schedule = {"A": [],
                    "B": [],
                    "C": [],
                    "D": []}
        for chrom in pop:
            first_hour = list(chrom[:10])
            sec_hour = list(chrom[10:20])
            third_hour = list(chrom[20:30])
            fourth_hour = list(chrom[30:])
            schedule["A"].extend(first_hour[:2] + sec_hour[:2] + third_hour[:2] + fourth_hour[:2])
            schedule["B"].extend(first_hour[2:5] + sec_hour[2:5] + third_hour[2:5] + fourth_hour[2:5])
            schedule["C"].extend(first_hour[5:8] + sec_hour[5:8] + third_hour[5:8] + fourth_hour[5:8])
            schedule["D"].extend(first_hour[8:] + sec_hour[8:] + third_hour[8:] + fourth_hour[8:])

        # fitness = 0
        # fitnesses = []
        cost = 0

        for student in self.residence_a:
            for course in student:
                for building in ["A", "B", "C", "D"]:
                    cost += self.distances["residence_a"][building] if self.encoding[course] in schedule[
                        building] else 0

        for student in self.residence_b:
            for course in student:
                for building in ["A", "B", "C", "D"]:
                    cost += self.distances["residence_b"][building] if self.encoding[course] in schedule[
                        building] else 0

        for student in self.residence_c:
            for course in student:
                for building in ["A", "B", "C", "D"]:
                    cost += self.distances["residence_c"][building] if self.encoding[course] in schedule[
                        building] else 0

        fitness = 1 / np.sqrt(cost) * 100

        return fitness

    def loop(self, generations: int) -> list:
        fitnesses = []
        fitness_sums = []
        for i in range(generations):
            fitnesses = [(idx, self.fitness([individual])) for idx, individual in enumerate(self.population)]
            # fitness = self.fitness(self.population)
            most_fit = sorted(fitnesses, key=operator.itemgetter(1), reverse=True)
            fitness_sums.append(most_fit[0][1])
            chromosomes = []

            # chromosomes = random.sample(self.population, 2)
            # chromes = self.crossover(chromosomes, rate=0.7)

            new_pop = []
            for idx, _ in most_fit[:self.n_keep]:
                parent = self.population[idx]
                children = [self.mutated_child(parent, rate=1) for _ in range(self.n_reproduce - 1)]
                children.append(parent)
                new_pop += children
            # assert len(new_pop) == len(self.population), "Length is not the same for populations"
            # if new_pop_fitness > fitness:
            #    self.population = new_pop
            #    fitnesses.append(new_pop_fitness)
            #    mutated_chromes = self.mutate(chromes, rate=0.7)

            self.population = new_pop
        plt.grid()
        plt.plot(fitness_sums)
        plt.xlabel("Generation")
        plt.ylabel("Total Fitness")
        plt.title("Total Fitness over the generations")
        plt.show()
        plt.close()
        print(f"Length of new population: {len(self.population)}")
        return self.population

    @staticmethod
    def crossover(chromosomes: list, rate: float) -> list:
        """
        A function that performs a crossover for the chromosomes at a probability of `rate`
        Args:
            chromosomes: A vector of two chromosomes
            rate: The probability of crossover

        Returns: List of crossovered items.

        """
        first_chromosome, second_chromosome = list(chromosomes)
        chrome_a = list(first_chromosome[:20]) + list(second_chromosome[20:])
        chrome_b = list(second_chromosome[:20]) + list(first_chromosome[20:])
        chromes = []
        random_num = random.random()
        if random_num < rate:
            chromes.append(chrome_a)
            chromes.append(chrome_b)
            return chromes
        else:
            return chromosomes

    @staticmethod
    def mutated_child(individual: list, rate: float) -> list:
        # TODO: Only slightly mutate with a strength based on the rate
        child = copy.deepcopy(individual)
        if random.random() < rate:
            random.shuffle(child)
        return child

    def __repr__(self):
        return f'A representation of the genetic algorithm class'


if __name__ == "__main__":
    gen = Genetic()
    new_pop = gen.loop(generations=1000)
    timetable_ = random.choice(new_pop)
    timetable = []
    for i in timetable_:
        timetable.append(gen.info[i])
    print(timetable)
