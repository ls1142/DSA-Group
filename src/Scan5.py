

all_requests = []

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
            temp_list = [int(num) for num in line.split() if num.isdigit()]
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

# Display output
print(f"Floors: {top_floor}, Capacity: {capacity}")
print(f"All requests: {all_requests}")

max_capacity = 4  # maximum capacity of the lift

# Define the initial floors
floors = all_requests
lift = []  # lift starts empty

def scan_alg(floors, lift, max_capacity):
    
    
    print("Floors before lift:")  
    for idx, floor in enumerate(floors):  
        print(f"Floor {idx}: {floor}")  

    # Lift going up
    for floor_count in range(len(floors)):  
        print(f"\nProcessing floor {floor_count}...")

        # Drop off passengers who requested this floor
        for person in lift[:]:  
            if person == floor_count:
                lift.remove(person)  
                print(f"Dropped off passenger {person} at floor {floor_count}")

        # Pick up passengers if there's space in the lift
        while floors[floor_count] and len(lift) < max_capacity:
            person = floors[floor_count].pop(0)  
            lift.append(person)  
            print(f"Picked up passenger {person} from floor {floor_count}")
            

        # If lift reaches max capacity, drop everyone off
        if len(lift) == max_capacity:
            print(f"Lift reached max capacity at floor {floor_count}, dropping everyone off!")
            for person in lift[:]:
                lift.remove(person)
                floors[person].append(person)
                print(f"Dropped off passenger {person} at floor {person}")
            print(f"Floors after dropping off at max capacity: {floors}")

        # Recheck if there's any pending passengers on this floor
        if floors[floor_count]:
            print(f"Pending requests on floor {floor_count}: {floors[floor_count]}")

    # If there are still passengers in the lift, drop them off
    if len(lift) > 0:
        print(f"\nRemaining passengers in the lift, continuing to drop them off: {lift}")

    # Lift going down (recheck the remaining passengers)
    for floor_count in range(len(floors) - 1, -1, -1):  
        print(f"\nProcessing floor {floor_count} during descent...")

        # Drop off passengers who requested this floor
        for person in lift[:]:  
            if person == floor_count:
                lift.remove(person)
                # Add the dropped off person back to their floor so they appear in final output
                floors[floor_count].append(person)
                print(f"Dropped off passenger {person} at floor {floor_count}")

    # pick up  if there's space in the lift 
        i = 0
        while i < len(floors[floor_count]) and len(lift) < max_capacity:
            # check if this person wants to go to a different floor,to stop lift picking people back up on way down 
            if floors[floor_count][i] != floor_count:  
                person = floors[floor_count].pop(i)  
                lift.append(person)  
                print(f"Picked up passenger {person} from floor {floor_count} during descent")
            else:
                # Skip this person as they want to go to the current floor, this stops the re picking up 
                print(f"Skipping passenger {floors[floor_count][i]} as they want to go to the current floor")
                i += 1

        # check for pending requests again as we descend
        if floors[floor_count]:
            print(f"Pending requests on floor {floor_count} during descent: {floors[floor_count]}")

    print("\nFloors after lift:") #pritns what our floors look like after lift each floor should only have numbers equal to that floor
    for idx, floor in enumerate(floors): 
        print(f"Floor {idx}: {floor}")  
    
   
    
   


# Run the function
scan_alg(floors, lift, max_capacity)


