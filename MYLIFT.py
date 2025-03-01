import time  # we are going to track execution time

all_requests = []  # used to store floor requests

def making_list_of_requests(list_type_of_requests):
    temp_list = []
    if len(list_type_of_requests) > 0:
        temp_list = [int(x) for x in list_type_of_requests if str(x).isdigit()]
    all_requests.append(temp_list)

# Read input from file
with open("input.txt", "r") as file:
    line_in_file = 0
    top_floor = 0
    capacity = 0

    for line in file:
        line = line.strip()
        line_in_file += 1

        if line_in_file == 1:
            # Changed this line to handle comma-separated numbers as well
            temp_list = [int(num) for num in line.replace(",", " ").split() if num.isdigit()]
            if len(temp_list) >= 2:
                top_floor, capacity = temp_list[0], temp_list[1]
            else:
                print("Error: First line must contain two numbers (floors, capacity).")
                exit()

        elif ":" in line:
            try:
                floor_part, requests_part = line.split(":", 1)
                floor = int(floor_part.strip())
                
                if floor > top_floor:
                    top_floor = floor 
                
                requests_part = requests_part.strip()
                list_type_of_requests = [int(num) for num in requests_part.replace(" ", "").split(",") if num.isdigit()]
                making_list_of_requests(list_type_of_requests)

            except ValueError:
                print(f"Skipping invalid line: {line.strip()}")

# Fill in any missing floors in all_requests
while len(all_requests) <= top_floor:
    all_requests.append([])

# display output
print(f"Floors: {top_floor}, Capacity: {capacity}")
print(f"All requests: {all_requests}")

# Define the sorting function from MYLIFT.py
def sort_requests(Queue):
    sorted_queue = []  # Create a new list to store sorted requests
    
    # Create a copy of Queue to work with
    queue_copy = Queue.copy()
    
    while queue_copy:  # Continue while there are elements
        lowest = float('inf')  # Reset lowest value for each iteration
        
        # Find the lowest value
        for j in queue_copy:
            if j < lowest:
                lowest = j
        
        sorted_queue.append(lowest)  # Add lowest to sorted_queue
        queue_copy.remove(lowest)  # Remove from original list
    
    return sorted_queue  # Return the sorted queue

def hybrid_scan_algorithm(floors, max_capacity, top_floor):
    start_time = time.time()
    lift = []  # lift starts empty
    total_floors = len(floors)
    
    # Track dropped-off passengers
    dropped_off_passengers = [[] for _ in range(total_floors)]
    
    print("Floors before lift:")  # print what the floors look before algorithm execution
    for idx, floor in enumerate(floors):  
        print(f"Floor {idx}: {floor}")
    
    # Continue until all floors are empty
    cycle_count = 0
    while any(floors):
        cycle_count += 1
        print(f"\n--- Starting cycle {cycle_count} ---")
        
        # Going up phase
        print("\n--- Going UP ---")
        for floor_count in range(total_floors):  
            print(f"\nProcessing floor {floor_count}...")

            # Drop off passengers who requested this floor
            for person in lift[:]:  
                if person == floor_count:
                    lift.remove(person)  
                    dropped_off_passengers[floor_count].append(person)  # Track dropped-off passengers
                    print(f"Dropped off passenger {person} at floor {floor_count}")

            # Pick up passengers if there's space in the lift
            while floors[floor_count] and len(lift) < max_capacity:
                person = floors[floor_count].pop(0)  # pop takes them off their floor
                lift.append(person)  # append adds them to lift
                print(f"Picked up passenger {person} from floor {floor_count}")

            print(f"Lift status: {lift}")
            print(f"Floors status: {floors}")
            
            # If lift reaches max capacity, sort and continue
            if len(lift) == max_capacity:
                print(f"Lift reached max capacity at floor {floor_count}, sorting the queue!")
                lift = sort_requests(lift)
                print(f"Sorted lift: {lift}")

        # We've reached the top floor, sort the queue and skip directly to the bottom
        if lift:
            print(f"\nReached the top floor. Current lift: {lift}")
            print("Sorting the queue before returning to the bottom floor...")
            lift = sort_requests(lift)
            print(f"Sorted lift: {lift}")
        
        print("\nSkipping directly to the bottom floor!")
        
        # Check if all floors are empty and lift is empty
        if not any(floors) and not lift:
            print("\nAll requests have been processed!")
            break
    
    # Make sure any remaining passengers in the lift are dropped off
    if lift:
        print(f"\nFinal passengers in the lift, dropping them off: {lift}")
        for person in lift[:]:
            print(f"Dropped off passenger {person} at floor {person}")
            dropped_off_passengers[person].append(person)  # Track dropped-off passengers
            lift.remove(person)

    print("\nFloors after lift:") 
    for idx, floor in enumerate(floors): 
        print(f"Floor {idx}: {floor}")  
    
    # Display dropped-off passengers
    print("\nDropped-off passengers:")
    for idx, passengers in enumerate(dropped_off_passengers):
        print(f"Floor {idx}: {passengers}")
    
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    print(f"\nExecution time: {execution_time:.2f} ms")
    
    return execution_time

# Set max capacity from input
max_capacity = capacity if capacity > 0 else 4  # default to 4 if not specified

# Create a copy of all_requests for the algorithm to use
floors_copy = [floor.copy() for floor in all_requests]

# Run the hybrid algorithm
hybrid_scan_algorithm(floors_copy, max_capacity, top_floor)
