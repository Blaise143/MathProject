import numpy as np
import pandas as pd
import random


class Genetic:

    def __init__(self, buildings=None, residences=None):
        data = pd.read_csv("data/students.csv")[["mandatory_1", "mandatory_2",
                                                 "mandatory_3", "elective_1",
                                                 "elective_2"]]
        self.data = np.array(data).tolist()
        info_ = []
        for i in data.columns:
            info_.extend(data[i].unique().tolist())
        self.info = dict(list(zip(range(40), list(sorted(set(info_))))))

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
        np.random.seed(42)
        for i in range(1):
            self.population.append(np.random.permutation(self.chromosome))



    def fitness(self, pop: list):
        schedule = {"A": [],
                    "B": [],
                    "C": [],
                    "D": []}
        for chrom in pop:
            first_hour = list(chrom[:10])
            sec_hour = list(chrom[10:20])
            third_hour = list(chrom[20:30])
            fourth_hour = list(chrom[30:])
            # print(len(first_hour), len(sec_hour), len(third_hour), len(fourth_hour))
            schedule["A"].extend(first_hour[:2] + sec_hour[:2] + third_hour[:2] + fourth_hour[:2])
            schedule["B"].extend(first_hour[2:5] + sec_hour[2:5] + third_hour[2:5] + fourth_hour[2:5])
            schedule["C"].extend(first_hour[5:8] + sec_hour[5:8] + third_hour[5:8] + fourth_hour[5:8])
            schedule["D"].extend(first_hour[8:] + sec_hour[8:] + third_hour[8:] + fourth_hour[8:])
        print(schedule)




if __name__ == "__main__":
    gen = Genetic()
    # gen.fitness(gen.population)
    # print(gen.population)
    # print(gen.info)
    #df = pd.read_csv("data/students.csv").drop("Unnamed: 0", axis=1)
    #print(df.head())
    #print(len(np.array(df.head()).tolist()))
    print(len(gen.data))