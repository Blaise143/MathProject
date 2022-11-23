class Building:
    def __init__(self, name, capacity: int) -> None:
        self._capacity = capacity
        self._name = name

    def name(self):
        return self._name

    def capacity(self) -> int:
        return self._capacity


class Residence:
    def __init__(self, capacity=10) -> None:
        self._capacity = capacity

    def capacity(self):
        return self._capacity


class Student:
    def __init__(self, res: Residence, courses: list):
        self.res = res
        self._courses = courses

    def __getitem__(self, item):
        assert item in ["Residence", "Courses"], "item should be either residence or courses"

        return self.res if item == "Residence" else self._courses


class Algo:

    def __init__(self, students: list):
        self.students = students
        self.distances = {
            "ThunderBird": {
                Building("A", capacity=20): 200,
                Building("B", capacity=30): 3982,
                Building("C", capacity=23): 922,
                Building("D", capacity=20): 3829
            },
            "WalterGage": {
                Building("A", capacity=20): 200,
                Building("B", capacity=30): 3982,
                Building("C", capacity=23): 922,
                Building("D", capacity=20): 3829
            },
            "Totem": {
                Building("A", capacity=20): 200,
                Building("B", capacity=30): 3982,
                Building("C", capacity=23): 922,
                Building("D", capacity=20): 3829
            }
        }

    def __repr__(self):
        return "The Goat Algorithm"
