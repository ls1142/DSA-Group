from Scan import scan_alg
from Look import Lift
import random
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np




def means(data: list) -> float:
    """calculates the mean of a dataset"""
    s = 0
    for i in range(0, len(data)):
        s += data[i]
    return s/len(data)


def standarddevations(data: list, mean: float) -> float:
    """calculates the standard devation of a dataset with mean 'mean'"""
    s = 0
    for i in range(0, len(data)):
        s += (data[i]-mean)**2
    unsquarerootedSD = s/len(data)
    return sqrt(unsquarerootedSD)



def generateFileData(floors:int,people:int)->None:
    data = generateData(floors, people)
    
    string = str(floors)+",1\n"
    for i in range(1,floors+1):
        if len(data[i-1]) != 0:
            string = string + "\n" + str(i) + ": "
        else:
            string = string + "\n" + str(i) + ":"
        for j in range(0,len(data[i-1])):
            if j != len(data[i-1])-1:
                string = string + str(data[i-1][j])+", "
            else:
                string = string + str(data[i-1][j])
    
    with open("input.txt", "w") as file:
        file.write(string)


def generateData(floors:int,people:int) -> list:
    data = []
    for i in range(0, floors):
        data.append([])
        
    for i in range(0,people):
        data[random.randint(0,floors-1)].append(random.randint(0,floors-1))
    return data

def generatePD(data: list, disc: int) -> list:
    s = 0; e = 5
    pd = []
    for i in range(0,disc):
        pd.append(0)
        
    lend = len(data)
    for i in range(0,len(data)):
        for j in range(1,disc):
            if data[i]<=(e-s)/disc*(j+1) and data[i]>(e-s)/disc*(j):
                pd[j]+=(1)/lend
    return pd


def test(testLength: int = 100, testFloors: int = 10, testPeople: int = 10, algorithm: callable = None):
    """Runs a test on the data, outputs and returns mean and standard deviation"""
    
    data = []
    for i in range(0,testLength):
        randomData = generateData(testFloors,testPeople)
        data.append(algorithm(randomData, [], 1))


    mean = means(data)
    sd = standarddevations(data, mean)
    print(f"average:{str(mean)}")
    print(f"standardDevation:{str(sd)}") 
    pd = generatePD(data, 20)
    
    pdz = []
    for i in range(0, 20):
        for j in range(0,round(5000/20)):
            pdz.append(pd[i])
    
    return mean,sd,pdz


if __name__ == "__main__":
    SAMPLES = 500
    FLOORS = 100
    PEOPLE = 1000000
    
    generateFileData(10,10)
    
    #mean, sd, pd = test(SAMPLES,FLOORS,PEOPLE,scan_alg)
    mean2, sd2, pd2 = test(round(SAMPLES/5),FLOORS,round(PEOPLE/10),Lift())
    #x = np.arange(0,5,0.001)
    #f = 1/sqrt(2*3.14159265359)*np.exp((-1/2)*((x-mean)/sd)**2)
    f2 = 1/sqrt(2*3.14159265359)*np.exp((-1/2)*((x-mean2)/sd2)**2)
    #g = np.array(pd)
    g2 = np.array(pd2)

    fig, ax = plt.subplots()
    
    
    #ax.plot(x,g,color='red',alpha=1.0)
    ax.plot(x,g2,color='green',alpha=1.0)
    
    
    #ax.plot(x,f,color='red',alpha=1.00,label="Scan")
    ax.plot(x,f2,color='green',alpha=1.00,label="Look(but not really)")
    #ax.fill_between(x,f,0,color='red',alpha=0.1)
    ax.fill_between(x,f2,0,color='green',alpha=0.1)
    plt.ylabel("Probability Density")
    plt.xlabel("Time(s)")
    plt.legend()
    plt.suptitle(f"Normal Distributions of Each Algorithm",fontsize=14, fontweight='bold')
    plt.title(f'{SAMPLES} samples per algorithm with {FLOORS} floors and {PEOPLE} people.',fontsize="8")
    plt.show()
