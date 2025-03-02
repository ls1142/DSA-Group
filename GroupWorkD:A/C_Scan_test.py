import random
from math import sqrt, pi, exp
import matplotlib.pyplot as plt
import numpy as np
import time
import signal

# Define a timeout handler
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Function timed out")

def calculate_mean(data: list) -> float:
    """Calculates the mean of a dataset"""
    return sum(data) / len(data) if data else 0

def calculate_standard_deviation(data: list, mean: float) -> float:
    """Calculates the standard deviation of a dataset"""
    return sqrt(sum((x - mean) ** 2 for x in data) / len(data)) if data else 0

def generate_data(floors: int, people: int) -> list:
    """Generates test data for floors and people"""
    data = [[] for _ in range(floors)]
    for _ in range(people):
        start_floor = random.randint(0, floors - 1)
        destination_floor = random.randint(0, floors - 1)
        while destination_floor == start_floor:
            destination_floor = random.randint(0, floors - 1)
        data[start_floor].append(destination_floor)
    return data

def flatten_data(data: list) -> list:
    """Flattens a list of lists into a single list"""
    return [person for sublist in data for person in sublist]

def run_with_timeout(func, args=(), kwargs={}, timeout_duration=60):
    """Run a function with a timeout"""
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_duration)
    
    try:
        result = func(*args, **kwargs)
        signal.alarm(0)  # Cancel the alarm
        return result, True
    except TimeoutException:
        print(f"Function timed out after {timeout_duration} seconds")
        return None, False
    except Exception as e:
        signal.alarm(0)
        print(f"Exception occurred: {e}")
        return None, False

def hybrid_scan_algorithm(flat_data: list, lift: list, start_floor: int) -> float:
    """Modified hybrid scan algorithm to work with test framework"""
    start_time = time.time()
    max_capacity = 4  # Default capacity
    top_floor = max(flat_data) if flat_data else 0
    floors = [[] for _ in range(top_floor + 1)]
    
    # Reconstruct floor requests from flat_data
    for request in flat_data:
        if 0 <= request <= top_floor:
            floors[request].append(request)
    
    while any(floors) or lift:
        # Going up
        for floor in range(start_floor, top_floor + 1):
            lift = [p for p in lift if p != floor]  # Drop off passengers
            while floors[floor] and len(lift) < max_capacity:
                lift.append(floors[floor].pop(0))
        
        # Going down
        for floor in range(top_floor, -1, -1):
            lift = [p for p in lift if p != floor]  # Drop off passengers
            while floors[floor] and len(lift) < max_capacity:
                lift.append(floors[floor].pop(0))
    
    end_time = time.time()
    return (end_time - start_time) * 1000  # Return execution time in ms

def test_algorithm(test_length=100, test_floors=10, test_people=10, algorithm=None, max_time_per_run=60):
    """Runs a test on the algorithm and computes statistics"""
    results = []
    successful_runs = 0
    
    for i in range(test_length):
        random_data = generate_data(test_floors, test_people)
        print(f"Generated test data for run {i+1}: {random_data}")
        
        flat_data = flatten_data(random_data)
        print(f"Flattened data: {flat_data}")
        
        result, success = run_with_timeout(algorithm, args=(flat_data, [], 0), timeout_duration=max_time_per_run)
        
        if success:
            results.append(result)
            successful_runs += 1
            print(f"Test {i+1} completed successfully")
        else:
            print(f"Test {i+1} failed - skipping this sample")
        
        if i >= 5 and successful_runs == 0:
            print("No successful runs after multiple attempts. Terminating test.")
            break
    
    if not results:
        print("No successful runs completed. Cannot calculate statistics.")
        return None, None, []
    
    mean_value = calculate_mean(results)
    sd_value = calculate_standard_deviation(results, mean_value)
    print(f"Mean: {mean_value}, Standard Deviation: {sd_value}, Successful runs: {successful_runs}/{test_length}")
    
    return mean_value, sd_value, results

if __name__ == "__main__":
    SAMPLES = 500
    FLOORS = 100
    PEOPLE = 1000
    MAX_TIME_PER_RUN = 60
    
    print(f"Running analysis with {SAMPLES} samples, {FLOORS} floors, and {PEOPLE} people")
    
    mean, sd, pd = test_algorithm(SAMPLES, FLOORS, PEOPLE, hybrid_scan_algorithm, max_time_per_run=MAX_TIME_PER_RUN)
    
    if mean is None:
        print("Analysis failed - couldn't calculate statistics")
        exit()
    
    x = np.linspace(0, 5, 1000)
    f = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mean) / sd) ** 2)

    
    plt.plot(x, f, color='red', label="Scan Algorithm")
    plt.fill_between(x, f, 0, color='red', alpha=0.1)
    plt.xlabel("Time (s)")
    plt.ylabel("Probability Density")
    plt.legend()
    plt.title(f"Normal Distribution of Scan Algorithm ({SAMPLES} samples)")
    plt.show()
