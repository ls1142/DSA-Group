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

def isLiftFull(people_in_lift): # checks to see if lift is full
    if people_in_lift == capacity:
        return True
    else: return False

def is_floor_empty(floor_request): # checks to see if there are any floor requests on that particular floor
    if len(floor_request) == 0:
        return True
    else: return False

def requests_completed(all_requests): # checks to see if there are no more requests across all floors
    floors_completed = 0
    for requests in all_requests:
        if len(requests) == 0:
            floors_completed += 1
    if floors_completed == top_floor:
        return True
    else: return False
    
def change_direction(current_floor, Up): # checks to see if lift has hit bottom or top floor
    if (current_floor == top_floor - 1) and Up == True: return True
    elif (current_floor == 0) and Up == False: return True
    else: return False

def leaving_lift(lift, current_floor): # takes people out the lift if their at the floor requested
    people_leaving = []
    for people in lift:
        if people == current_floor + 1:
            people_leaving.append(people)
    for people in people_leaving:
        lift.remove(people)
    return lift

def requests_in_direction_complete(all_requests, current_floor, Up): # checks if all requests in direction lift is travelling is completed
    if Up == True:
        difference = (top_floor - 1) - current_floor
        for floor in range(current_floor, top_floor - 1):
            if len(all_requests[floor]) == 0:
                difference -= 1
    elif Up == False:
        difference = current_floor
        for floor in range(current_floor, -1, -1):
            if len(all_requests[floor]) == 0:
                difference -= 1
    if difference == 0:
        return True
    else: return False

all_requests = []
lift = []
line_in_file = 0
top_floor = 0
current_floor = 0
Up = True
completed = False

with open("input.txt", "r") as file:
    for line in file:
        temp_list = []
        line_in_file += 1
        if line_in_file == 1:
            for characters in list(line): 
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
            making_list_of_requests(list_type_of_requests) # processes requests

def upLift(lift, all_requests, current_floor, completed, Up): # lift going up 
    Up = True
    for floor in range(current_floor, top_floor): # goes through all floors between current floor and top floor 
        leaving_lift(lift, current_floor) # takes people out lift if the floor is the one they requested
        if requests_completed(all_requests) == True and len(lift) == 0:
            completed = True
            None # need to add time here (return time)
        else:
            people_added = []
            for people in all_requests[floor]:
                if isLiftFull(len(lift)) == False: # adds people to lift if its not full
                    lift.append(people)
                    people_added.append(people)
                elif isLiftFull(len(lift)) == True: break # moves to next floor if lift full
            for people in people_added:
                all_requests[floor].remove(people) # removes requests from people who have been added to lift
        if requests_in_direction_complete(all_requests, current_floor, Up) == True:
            if requests_completed(all_requests) == True and len(lift) > 0: # if all requests have been completed but people still in lift
                continue
            elif requests_completed(all_requests) == True and len(lift) == 0: # checks if all requests have been completed
                completed = True
                return lift, all_requests, current_floor, completed, Up
        if change_direction(current_floor, Up) == True: # checks to see if top floor has been reached to change direction 
            Up = False
            break
        else: 
            print(current_floor)
            current_floor += 1
        print(lift)
        print(all_requests)
    Up = False
    print(lift)
    print(all_requests)
    print(current_floor)
    if requests_completed(all_requests) == True and len(lift) == 0: # checks if all requests have been completed 
        completed = True
        return lift, all_requests, current_floor, completed, Up
    else: return lift, all_requests, current_floor, completed, Up

def downLift(lift, all_requests, current_floor, completed, Up):
    Up = False
    for floor in range(current_floor, -1, -1): # moves from current down to 0 floor
        leaving_lift(lift, current_floor) # takes people out lift if the floor is the one they requested
        if requests_completed(all_requests) == True and len(lift) == 0: # checks if all requests have been completed
            completed = True
            None # need to add time here (return time)
        else:
            people_added = []
            for people in all_requests[floor]:
                if isLiftFull(len(lift)) == False: # adds people to lift if its not full
                    lift.append(people)
                    people_added.append(people)
                elif isLiftFull(len(lift)) == True: break # moves to next floor if lift full 
            for people in people_added:
                all_requests[floor].remove(people) # removes requests from people who have been added to lift
        if requests_in_direction_complete(all_requests, current_floor, Up) == True:
            if requests_completed(all_requests) == True and len(lift) > 0: # if all requests have been completed but people still in lift
                continue
            elif requests_completed(all_requests) == True and len(lift) == 0: 
                completed = True
                return lift, all_requests, current_floor, completed, Up
        if change_direction(current_floor, Up) == True: # checks if lift has hit bottom floor
            Up = True
            break
        else: 
            print(current_floor)
            current_floor -= 1
        print(lift)
        print(all_requests)
    Up = True
    print(lift)
    print(current_floor)
    print(all_requests)
    if requests_completed(all_requests) == True and len(lift) == 0: # checks if all requests have been fulfilled and people on lift have been sent to their floors
        completed = True
        return lift, all_requests, current_floor, completed, Up
    else: return lift, all_requests, current_floor, completed, Up

def Lift(lift, all_requests, current_floor, completed, Up): # loops up and down till all requests have been fulfilled 
    while completed == False:
        if Up == True:
            lift, all_requests, current_floor, completed, Up = upLift(lift, all_requests, current_floor, completed, Up)
        elif Up == False:
            lift, all_requests, current_floor, completed, Up = downLift(lift, all_requests, current_floor, completed, Up)

Lift(lift, all_requests, current_floor, completed, Up)