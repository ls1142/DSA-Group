import time #we are going to track exacution time 

all_requests = []# used to store floor requests 

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

# display output
print(f"Floors: {top_floor}, Capacity: {capacity}")
print(f"All requests: {all_requests}")

max_capacity = 4  # maximum capacity of the lift

# Define the initial floors
floors = all_requests
lift = []  # lift starts empty

def scan_alg(floors, lift, max_capacity):
    start_time = time.time()
    
    print("Floors before lift:")  #print what the floors look before algorithm exacutuion
    for idx, floor in enumerate(floors):  
        print(f"Floor {idx}: {floor}")  

    # lift going up
    for floor_count in range(len(floors)):  
        print(f"\nProcessing floor {floor_count}...")

        # drop off passengers who requested this floor
        for person in lift[:]:  
            if person == floor_count:
                lift.remove(person)  
                # Add the passenger to their floor when dropped off
                floors[floor_count].append(person)
                print(f"Dropped off passenger {person} at floor {floor_count}")

        # pick up passengers if there's space in the lift
        while floors[floor_count] and len(lift) < max_capacity:
            person = floors[floor_count].pop(0) #pop takes them off there floor,0 means we take first so it works as a queue 
            lift.append(person)  #append adds them to lift
            print(f"Picked up passenger {person} from floor {floor_count}")#shows us who was picked up from where,helps with trackinh movement for de bigging
            

        # if lift reaches max capacity, drop everyone off
        if len(lift) == max_capacity:
            print(f"Lift reached max capacity at floor {floor_count}, dropping everyone off!")
            for person in lift[:]:#copy of lift
                lift.remove(person)#remove them 
                floors[person].append(person)#add to floor
                print(f"Dropped off passenger {person} at floor {person}")#shows whos dropped of where to keep track for debugging
            print(f"Floors after dropping off at max capacity: {floors}")

        # recheck if theres passengers on this floor
        if floors[floor_count]:
            print(f"Pending requests on floor {floor_count}: {floors[floor_count]}")

    # if there are still passengers in the lift drop them off
    if len(lift) > 0:
        print(f"\nRemaining passengers in the lift, continuing to drop them off: {lift}")
        for person in lift[:]:
            lift.remove(person)
            floors[person].append(person)
            print(f"Dropped off passenger {person} at floor {person}")

    # start down wards journey 
    for floor_count in range(len(floors) - 1, -1, -1):  #looping from highest floor
        print(f"\nProcessing floor {floor_count} during descent...")#show what floor is being processed

        # drop off passengers who requested this floor
        for person in lift[:]:  #using copy to not mess with origonal 
            if person == floor_count:#xheck request for right floor
                lift.remove(person)#take from lif
                # add the dropped off person back to their floor 
                floors[floor_count].append(person)
                print(f"Dropped off passenger {person} at floor {floor_count}")

        # pick up if there's space in the lift 
        i = 0 #set i to 0 for going theough floor to check people waiitimgh , tallow checks to stop re picking up on way back down 
        while i < len(floors[floor_count]) and len(lift) < max_capacity:
            # check if this person wants to go to a different floor,to stop lift picking people back up on way down 
            if floors[floor_count][i] != floor_count:  
                person = floors[floor_count].pop(i)  #take off floor
                lift.append(person)  #add to list 
                print(f"Picked up passenger {person} from floor {floor_count} during descent")
            else:
                # skip this person as they want to go to the current floor this stops the re picking up 
                print(f"Skipping passenger {floors[floor_count][i]} as they want to go to the current floor")
                i += 1#increase for 1

        # check for pending requests again as we descend
        if floors[floor_count]:
            print(f"Pending requests on floor {floor_count} during descent: {floors[floor_count]}")

    # Make sure any remaining passengers in the lift are dropped off
    if len(lift) > 0:
        print(f"\nFinal remaining passengers in the lift, dropping them off: {lift}")
        for person in lift[:]:
            lift.remove(person)
            floors[person].append(person)
            print(f"Dropped off passenger {person} at floor {person}")

    print("\nFloors after lift:") #pritns what our floors look like after lift each floor should only have numbers equal to that floor
    for idx, floor in enumerate(floors): 
        print(f"Floor {idx}: {floor}")  
    
    end_time = time.time()
    
    return (end_time - start_time) * 1000
    
# Run the function
print(scan_alg(floors, lift, max_capacity))