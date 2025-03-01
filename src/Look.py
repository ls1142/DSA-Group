import time

def making_list_of_requests(list_type_of_requests): # makes a list of each floors requests
    temp_list = [] 
    if len(list_type_of_requests) > 1: # checks if there are no requests 
        list_type_of_requests = "".join(list_type_of_requests) 
        list_type_of_requests = list_type_of_requests.strip() # gets rid of \n at ends of requests
        list_type_of_requests = list_type_of_requests.split(", ") # list is only numbers now 
        for request in list_type_of_requests:
            temp_list.append(int(request))
        all_requests.append(temp_list) # adds each floors of requests to a list
    elif len(list_type_of_requests) == 1: # floor with no requests
        list_type_of_requests.pop(0) 
        all_requests.append(list_type_of_requests)
    elif len(list_type_of_requests) == 0: # floor with no requests
        all_requests.append(list_type_of_requests)
    return all_requests

def isLiftFull(people_in_lift, capacity): # checks to see if lift is full
    if people_in_lift == capacity:
        return True
    else: return False

def is_floor_empty(floor_request): # checks to see if there are any floor requests on that particular floor
    if len(floor_request) == 0:
        return True
    else: return False

def requests_completed(all_requests, top_floor): # checks to see if there are no more requests across all floors
    floors_completed = 0
    for requests in all_requests:
        if len(requests) == 0:
            floors_completed += 1
    if floors_completed == top_floor:
        return True
    else: return False
    
def change_direction(current_floor, Up, top_floor): # checks to see if lift has hit bottom or top floor
    if (current_floor + 1 == top_floor) and Up == True: return True
    elif (current_floor == 0) and Up == False: return True
    else: return False

def leaving_lift(lift, current_floor): # takes people out the lift if their at the floor requested
    people_leaving = []
    for people in lift:
        if people == current_floor:
            people_leaving.append(people)
    for people in people_leaving:
        lift.remove(people)
    return lift

def requests_in_direction_complete(all_requests, current_floor, Up, top_floor): # checks if all requests in direction lift is travelling is completed
    if Up == True:
        difference = top_floor - current_floor
        for floor in range(current_floor, top_floor):
            if len(all_requests[floor]) == 0:
                difference -= 1
    elif Up == False:
        difference = current_floor + 1
        for floor in range(current_floor, -1, -1):
            if len(all_requests[floor]) == 0:
                difference -= 1
    if difference == 0:
        return True
    else: return False

def people_in_lift_requests(current_floor, lift, top_floor): # checks if there are more people there are going down compared to up 
    people_up = 0
    people_down = 0
    for requests in lift:
        if requests > current_floor:
            people_up += 1
        elif requests < current_floor:
            people_down += 1
    if people_up > people_down:
        return True
    elif people_up < people_down:
        return False
    elif people_up == people_down: # if equal then bases it on how close lift is to groud or top floor
        difference_bottom = current_floor
        difference_top = top_floor - current_floor
        if difference_top > difference_bottom:
            return False
        else: return True

all_requests = []
lift = []
current_floor = 0
Up = True
completed = False

def read_file(top_floor):
    line_in_file = 0
    with open("input.txt", "r") as file:
        temp_list = []
        for line in file:
            line_in_file += 1
            if line_in_file == 1:
                for characters in line.strip().split(","): 
                    if characters.isnumeric(): # gets rid of all the characters in the line except for numbers
                        temp_list.append(int(characters)) # adds them as integers to a different list
                amount_of_floors = temp_list[0]
                capacity = temp_list[1]
            elif ":" in list(line): # checks for the lines of text with the requests
                list_type_of_requests = list(line)
                temp_list2 = []
                index = list_type_of_requests.index(":")
                if index == 1: # checks if it is a single digit floor
                    temp_list2.append(list_type_of_requests[0]) # adds floor num to a list
                    floor = int(temp_list2[0]) 
                    if floor > top_floor:
                        top_floor = floor # sees which floor is highest and makes it top floor 
                    for x in range(0, 2):
                        list_type_of_requests.pop(0) # gets rid of the n: from line 
                elif index > 1: # checks if floor has more than a single digit
                    for x in range(0, index): # goes through numbers before :
                        temp_list2.append(list_type_of_requests[0]) 
                        list_type_of_requests.pop(0) # removes numbers before :
                        if x == index - 1:
                            list_type_of_requests.pop(0) # removes the :
                            floor = int("".join(temp_list2)) # joins the temp list together to make the floor number
                            if floor > top_floor:
                                top_floor = floor
                all_requests = making_list_of_requests(list_type_of_requests) # processes requests
        return all_requests, capacity, amount_of_floors, top_floor

def upLift(lift, all_requests, capacity, current_floor, completed, Up, top_floor): # lift going up 
    Up = True
    for floor in range(current_floor, top_floor): # goes through all floors between current floor and top floor 
        leaving_lift(lift, current_floor) # takes people out lift if the floor is the one they requested
        if requests_completed(all_requests, top_floor) == True and len(lift) == 0:
            completed = True
            return lift, all_requests, current_floor, completed, Up
        else:
            people_added = []
            for people in all_requests[floor]:
                if isLiftFull(len(lift), capacity) == False: # adds people to lift if its not full
                    lift.append(people)
                    people_added.append(people)
                elif isLiftFull(len(lift), capacity) == True: break # moves to next floor if lift full
            for people in people_added:
                all_requests[floor].remove(people) # removes requests from people who have been added to lift
        if requests_in_direction_complete(all_requests, current_floor, Up, top_floor) == True:
            if requests_completed(all_requests, top_floor) == True and len(lift) > 0: # if all requests have been completed but people still in lift
                if people_in_lift_requests(current_floor, lift, top_floor) == True:
                    None
                else:
                    Up = False
                    return lift, all_requests, current_floor, completed, Up
            elif requests_completed(all_requests, top_floor) == True and len(lift) == 0: # checks if all requests have been completed
                completed = True
                return lift, all_requests, current_floor, completed, Up
            elif people_in_lift_requests(current_floor, lift, top_floor) == True:
                None
            else:
                Up = False 
                return lift, all_requests, current_floor, completed, Up
        if change_direction(current_floor, Up, top_floor) == True: # checks to see if top floor has been reached to change direction 
            Up = False
            break
        else:
            print(all_requests)
            print(lift)
            print(current_floor)
            current_floor += 1
    Up = False
    return lift, all_requests, current_floor, completed, Up

def downLift(lift, all_requests, capacity, current_floor, completed, Up, top_floor):
    Up = False
    for floor in range(current_floor, -1, -1): # moves from current down to 0 floor
        leaving_lift(lift, current_floor) # takes people out lift if the floor is the one they requested
        if requests_completed(all_requests, top_floor) == True and len(lift) == 0: # checks if all requests have been completed
            completed = True
            return lift, all_requests, current_floor, completed, Up
        else:
            people_added = []
            for people in all_requests[floor]:
                if isLiftFull(len(lift), capacity) == False: # adds people to lift if its not full
                    lift.append(people)
                    people_added.append(people)
                elif isLiftFull(len(lift), capacity) == True:
                    break # moves to next floor if lift full 
            for people in people_added:
                all_requests[floor].remove(people) # removes requests from people who have been added to lift
        if requests_in_direction_complete(all_requests, current_floor, Up, top_floor) == True:
            if requests_completed(all_requests, top_floor) == True and len(lift) > 0: # if all requests have been completed but people still in lift
                if people_in_lift_requests(current_floor, lift, top_floor) == False:
                    None
                else:
                    Up = True
                    return lift, all_requests, current_floor, completed, Up
            elif requests_completed(all_requests, top_floor) == True and len(lift) == 0: 
                completed = True
                return lift, all_requests, current_floor, completed, Up
            elif people_in_lift_requests(current_floor, lift, top_floor) == False:
                None
            else:
                Up = True
                return lift, all_requests, current_floor, completed, Up
        if change_direction(current_floor, Up, top_floor) == True: # checks if lift has hit bottom floor
            Up = True
            return lift, all_requests, current_floor, completed, Up
        else:
            print(all_requests)
            print(lift)
            print(current_floor)
            current_floor -= 1
    Up = True
    return lift, all_requests, current_floor, completed, Up

def Lift(lift = [], all_requests = [], current_floor = 0, completed = False, Up = True): # loops up and down till all requests have been fulfilled 
    start_time = time.time()
    all_requests, capacity, amount_of_floors, top_floor = read_file(0)
    while completed == False:
        if Up == True:
            lift, all_requests, current_floor, completed, Up = upLift(lift, all_requests, capacity, current_floor, completed, Up, top_floor)
        elif Up == False:
            lift, all_requests, current_floor, completed, Up = downLift(lift, all_requests, capacity, current_floor, completed, Up, top_floor)
    end_time = time.time()
    return (end_time - start_time) * 1000


print(Lift(lift, all_requests, current_floor, completed, Up))