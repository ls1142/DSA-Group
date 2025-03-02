from Scan6 import scan_alg
import random
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
import time
import signal

# Define a timeout handler
class TimeoutException(Exception):
    pass
from Scan6 import scan_alg
from MYLIFT import hybrid_scan_algorithm
from Look3 import Lift
import random
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
import time
import signal

# Define a timeout handler
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Function timed out")

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

def generateFileData(floors:int,people:int,floorIndex:int)->None:
    data = generateData(floors, people,floorIndex)
    string = str(floors)+",1\n"
    for i in range(1,floors+1):
        if len(data[i-1]) == 0:
            string = string + "\n" + str(i) + ":"
        else:
            string = string + "\n" + str(i) + ": "
        for j in range(0,len(data[i-1])):
            if j != len(data[i-1])-1:
                string = string + str(data[i-1][j])+" , "
            else:
                string = string + str(data[i-1][j])
    with open("DSA-Group-main/GroupWorkD_A/input.txt", "w") as file:
        file.write(string)

def generateData(floors:int,people:int,floorIndex:int) -> list:
    data = []
    for i in range(0, floors):
        data.append([])
    for i in range(0,people):
        data[random.randint(0,floors-1)].append(random.randint(floorIndex,floors-1+floorIndex))
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

def run_with_timeout(func, args=(), kwargs={}, timeout_duration=60):
    """Run a function with a timeout"""
    # Set the timeout handler
    #signal.signal(signal.SIGALRM, timeout_handler)
    #signal.alarm(timeout_duration)
    
    try:
        result = func(*args, **kwargs)
        # Cancel the alarm if function completes
        #signal.alarm(0)
        return result, True
    except TimeoutException:
        # Function timed out
        print(f"Function timed out after {timeout_duration} seconds")
        return None, False
    except Exception as e:
        # Other exception occurred
        #signal.alarm(0)
        print(f"Exception occurred: {e}")
        return None, False

def test(testLength: int = 100, testFlors: int = 10, testPeople: int = 10, algorithm: callable = None, max_time_per_run=60, floorIndex: int = 0):
    """Runs a test on the data, outputs and returns mean and standard deviation"""
    data = []
    successful_runs = 0
    
    for i in range(0, testLength):
        generateFileData(testFlors, testPeople, floorIndex)
        #print(f"Running test {i+1}/{testLength}...")
        
        # Run with timeout
        start_time = time.time()
        result, success = run_with_timeout(
            algorithm, 
            args=([], [], 1), 
            timeout_duration=max_time_per_run
        )
        
        if success:
            data.append(result)
            successful_runs += 1
            print(f"Test {i+1} completed in {time.time() - start_time:.2f} seconds")
        else:
            print(f"Test {i+1} failed - skipping this sample")
        
        # Option to quit early if too many failures
        if i >= 5 and successful_runs == 0:
            print("No successful runs after multiple attempts. Terminating test.")
            break
    
    if not data:
        print("No successful runs completed. Cannot calculate statistics.")
        return None, None, []
    
    mean = means(data)
    sd = standarddevations(data, mean)
    print(f"average:{str(mean)}")
    print(f"standardDevation:{str(sd)}")
    print(f"Successful runs: {successful_runs}/{testLength}")
    
    pd = generatePD(data, 20)
    pdz = []
    for i in range(0, 20):
        for j in range(0, round(5000/20)):
            pdz.append(pd[i])
    return mean, sd, pdz

if __name__ == "__main__":
    # Reduced parameters for more reasonable runtime
    SAMPLES = 500  # Reduced from 500
    FLOORS = 100 # Reduced from 100
    PEOPLE = 10000  # Reduced from 10000
    MAX_TIME_PER_RUN = 60  # Maximum seconds per algorithm run
    
    print(f"Running analysis with {SAMPLES} samples, {FLOORS} floors, and {PEOPLE} people")
    print(f"Each run will timeout after {MAX_TIME_PER_RUN} seconds")
    
    print("scan")
    mean, sd, pd = test(SAMPLES, FLOORS, PEOPLE, scan_alg, max_time_per_run=MAX_TIME_PER_RUN)
    print("look")
    mean, sd, pd = test(SAMPLES, FLOORS, PEOPLE, Lift, max_time_per_run=MAX_TIME_PER_RUN, floorIndex=1)
    print("hybrid")
    mean, sd, pd = test(SAMPLES, FLOORS, PEOPLE, hybrid_scan_algorithm, max_time_per_run=MAX_TIME_PER_RUN)
    
    if mean is None:
        print("Analysis failed - couldn't calculate statistics")
        exit()
    
    x = np.arange(0, 5, 0.001)
    f = 1/sqrt(2*3.14159265359)*np.exp((-1/2)*((x-mean)/sd)**2)
    g = np.array(pd)
    
    fig, ax = plt.subplots()
    ax.plot(x, f, color='red', alpha=1.00, label="Scan")
    ax.fill_between(x, f, 0, color='red', alpha=0.1)
    plt.ylabel("Probability Density")
    plt.xlabel("Time(s)")
    plt.legend()
    plt.suptitle(f"Normal Distribution of Scan Algorithm", fontsize=14, fontweight='bold')
    plt.title(f'{SAMPLES} samples with {FLOORS} floors and {PEOPLE} people.', fontsize="8")
    plt.show()



def timeout_handler(signum, frame):
    raise TimeoutException("Function timed out")

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
        string = string + "\n" + str(i) + ":"
        for j in range(0,len(data[i-1])):
            if j != len(data[i-1])-1:
                string = string + str(data[i-1][j])+","
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

def run_with_timeout(func, args=(), kwargs={}, timeout_duration=60):
    """Run a function with a timeout"""
    # Set the timeout handler
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_duration)
    
    try:
        result = func(*args, **kwargs)
        # Cancel the alarm if function completes
        signal.alarm(0)
        return result, True
    except TimeoutException:
        # Function timed out
        print(f"Function timed out after {timeout_duration} seconds")
        return None, False
    except Exception as e:
        # Other exception occurred
        signal.alarm(0)
        print(f"Exception occurred: {e}")
        return None, False

def test(testLength: int = 100, testFlors: int = 10, testPeople: int = 10, algorithm: callable = None, max_time_per_run=60):
    """Runs a test on the data, outputs and returns mean and standard deviation"""
    data = []
    successful_runs = 0
    
    for i in range(0, testLength):
        randomData = generateData(testFlors, testPeople)
        print(f"Running test {i+1}/{testLength}...")
        
        # Run with timeout
        start_time = time.time()
        result, success = run_with_timeout(
            algorithm, 
            args=(randomData, [], 1), 
            timeout_duration=max_time_per_run
        )
        
        if success:
            data.append(result)
            successful_runs += 1
            print(f"Test {i+1} completed in {time.time() - start_time:.2f} seconds")
        else:
            print(f"Test {i+1} failed - skipping this sample")
        
        # Option to quit early if too many failures
        if i >= 5 and successful_runs == 0:
            print("No successful runs after multiple attempts. Terminating test.")
            break
    
    if not data:
        print("No successful runs completed. Cannot calculate statistics.")
        return None, None, []
    
    mean = means(data)
    sd = standarddevations(data, mean)
    print(f"average:{str(mean)}")
    print(f"standardDevation:{str(sd)}")
    print(f"Successful runs: {successful_runs}/{testLength}")
    
    pd = generatePD(data, 20)
    pdz = []
    for i in range(0, 20):
        for j in range(0, round(5000/20)):
            pdz.append(pd[i])
    return mean, sd, pdz

if __name__ == "__main__":
    # Reduced parameters for more reasonable runtime
    SAMPLES = 50  # Reduced from 500
    FLOORS = 10 # Reduced from 100
    PEOPLE = 100  # Reduced from 10000
    MAX_TIME_PER_RUN = 60  # Maximum seconds per algorithm run
    
    print(f"Running analysis with {SAMPLES} samples, {FLOORS} floors, and {PEOPLE} people")
    print(f"Each run will timeout after {MAX_TIME_PER_RUN} seconds")
    
    generateFileData(10, 10)
    mean, sd, pd = test(SAMPLES, FLOORS, PEOPLE, scan_alg, max_time_per_run=MAX_TIME_PER_RUN)
    
    if mean is None:
        print("Analysis failed - couldn't calculate statistics")
        exit()
    
    x = np.arange(0, 5, 0.001)
    f = 1/sqrt(2*3.14159265359)*np.exp((-1/2)*((x-mean)/sd)**2)
    g = np.array(pd)
    
    fig, ax = plt.subplots()
    ax.plot(x, f, color='red', alpha=1.00, label="Scan")
    ax.fill_between(x, f, 0, color='red', alpha=0.1)
    plt.ylabel("Probability Density")
    plt.xlabel("Time(s)")
    plt.legend()
    plt.suptitle(f"Normal Distribution of Scan Algorithm", fontsize=14, fontweight='bold')
    plt.title(f'{SAMPLES} samples with {FLOORS} floors and {PEOPLE} people.', fontsize="8")
    plt.show()


