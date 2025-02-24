import time

person_x = 3  # person x requests floor 3 stk
person_y = 1  # person y requests floor 1 stk
person_z = 2  # person z requests floor 2 stk
person_v = 4  # person v requests floor 4 (this is an issue, since it should be within the rang) stk
person_k = 3  # person k requests floor 3 stk
person_t = 3  # person t requests floor 3 stk

max_capacity = 3  # maximum capacity of the lift stk

# define the initial floors stk
ground_floor = [person_x, person_t, person_k]  
floor1 = []  
floor2 = [person_v]  # person v is requesting floor 4, wich doesnt exist in the rang stk
floor3 = [person_y, person_z]  

persons = [person_v, person_x, person_y, person_z]
floors = [ground_floor, floor1, floor2, floor3]  # list of floors stk
lift = []  # lift starts empty stk

# requested floors for each person stk
person_requests = {
    person_x: 3,
    person_y: 1,
    person_z: 2,
    person_v: 4,  # invalid floor request (4), wich is causing the indexerror stk
    person_k: 3,
    person_t: 3,
}

def scan_alg(floors, lift, max_capacity):
    start_time = time.time()
    
    # what the floors are before processing the requests stk
    print("floors before lift:")  
    for idx, floor in enumerate(floors):  
        print(f"floor {idx}: {floor}")  

    # lift going up stk
    for floor_count in range(len(floors)):  # loop upwards through floors stk
        # pick up passengers from the current floor stk
        while floors[floor_count] and len(lift) < max_capacity:  # while there are people and lift isnt full stk
            person = floors[floor_count].pop(0)  # take from floor stk
            lift.append(person)  # add to lift stk

        # drop off passengers at their requested floor stk
        for person in lift[:]:  
            requested_floor = person_requests.get(person)  # get the requested floor for the person stk
            
            # check if the requested floor is within valid rang stk
            if requested_floor is not None and 0 <= requested_floor < len(floors):
                if requested_floor == floor_count:  # if this is their requested floor stk
                    lift.remove(person)  # remove from lift stk
                    floors[requested_floor].append(person)  # drop them off at their requested floor stk

        # if lift reaches max capacity, drop everyone off and come back stk
        if len(lift) == max_capacity:
            print(f"lift reached max capacity at floor {floor_count}, dropping everyone off!")
            while lift:
                person = lift.pop(0)
                requested_floor = person_requests.get(person)
                
                # ensure the requested floor is valid before dropping off stk
                if requested_floor is not None and 0 <= requested_floor < len(floors):
                    floors[requested_floor].append(person)  # drop person at requested floor stk

    # print passengers in the lift after going up stk
    print(f"\npassengers in the lift after going up: {lift}")

    # lift going down stk
    for floor_count in range(len(floors) - 1, -1, -1):  # loop downwards through floors stk
        # drop off passengers at their floor stk
        for person in lift[:]:  
            requested_floor = person_requests.get(person)  # get the requested floor for the person stk
            
            # check if the requested floor is within valid rang stk
            if requested_floor is not None and 0 <= requested_floor < len(floors):
                if requested_floor == floor_count:  # if this is their requested floor stk
                    lift.remove(person)  # remove from lift stk
                    floors[requested_floor].append(person)  # drop them off at their requested floor stk

    # print floors after processing stk
    print("\nfloors after lift:") 
    for idx, floor in enumerate(floors): 
        print(f"floor {idx}: {floor}")  
    
    end_time = time.time()
    time_difference = (end_time - start_time) * 1000
    return time_difference

# call the function and return the time taken stk
scan_alg(floors, lift, max_capacity)
