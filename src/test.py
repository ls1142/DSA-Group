from rough_lift import scan_alg
import random
from math import sqrt


algorithm = scan_alg


def means(data: list):
    """calculates the mean of a dataset"""
    s = 0
    for i in range(0, len(data)):
        s += data[i]
    return s/len(data)


def standarddevations(data: list, mean: float):
    """calculates the standard devation of a dataset with mean 'mean'"""
    s = 0
    for i in range(0, len(data)):
        s += (data[i]-mean)**2
    unsquarerootedSD = s/len(data)
    return sqrt(unsquarerootedSD)


def test(testLength: int = 100):
    """Runs a test on the data, outputs and returns mean and standard deviation"""
    data = []
    for i in range(0,testLength):
        randomData = []
        data.append(algorithm(randomData))

    mean = means(data)
    sd = standarddevations(data, mean)
    print(f"average:{str(mean)}")
    print(f"standardDevation:{str(sd)}")
    return mean,sd


if __main__ == "__name__":
    test()
