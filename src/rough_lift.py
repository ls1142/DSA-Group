#  requested floors,STK
import time 
start_time = time.time() #start time 

person_x = 3  # person X requests floor 3,STK
person_y = 1  # person Y requests floor 1,STK
person_z = 2  # person Z requests floor 2,STK
person_v = 4 # person Z requests floor 4,STK

max_capacity = 3 

# Define the initial floors,STK
ground_floor = [person_x]  
floor1 = []  
floor2 = [person_v]  
floor3 = [person_y, person_z]  

floors = [ground_floor, floor1, floor2, floor3]  # list of floors,STK
lift = []  # lift starts empty,STK


# what the floor are before we process tge requests,STK
print("Floors before lift:")  
for idx, floor in enumerate(floors):  
    print(f"Floor {idx}: {floor}")  

# lift going up,STK
for floor_count in range(len(floors)):  # loop through upwards,STK
    # pick up passengers from the current floor,STK
    while floors[floor_count]:  # while there are people on the floor,STK

        person = floors[floor_count].pop(0)  # take from floor,STK

        if (person >= 0) and person <4:
            lift.append(person)  # add them to the lift,STK
        else:
            continue

    # drop off passengers at their requested floor,STK
    for person in lift[:]:  
        if person == floor_count:  # if this is their requested floor,STK
            lift.remove(person)  # remove from lift,STK
            floors[floor_count].append(person)  # drop them off,STK

# print passengers in the lift after going up,STK
print(f"\nPassengers in the lift after going up: {lift}")  # STK

# lift going down,STK
for floor_count in range(len(floors) - 1, -1, -1):  # loop through downwards,STK
    # drop off passengers at their floor,STK
    for person in lift[:]:  

        if person == floor_count:  # if this is their requested floor,STK
            lift.remove(person)  # remove them from the lift,STK
            floors[floor_count].append(person)  # drop them off,STK

end_time = time.time()

print("\nFloors after lift:") 
for idx, floor in enumerate(floors): 
    print(f"Floor {idx}: {floor}")  

print(f"Execution time for lift  : {end_time - start_time:.6f} seconds")

