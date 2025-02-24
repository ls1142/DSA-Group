def making_list_of_requests(list_type_of_requests):
    temp_list = []
    if len(list_type_of_requests) > 1:
        list_type_of_requests = "".join(list_type_of_requests)
        list_type_of_requests = list_type_of_requests.strip()
        list_type_of_requests = list_type_of_requests.split(", ")
        for request in list_type_of_requests:
            temp_list.append(int(request))
        all_requests.append(temp_list)
    elif len(list_type_of_requests) == 1:
        list_type_of_requests.pop(0)
        all_requests.append(list_type_of_requests)
    elif len(list_type_of_requests) == 0:
        all_requests.append(list_type_of_requests)

def isLiftFull(people_in_lift):
    if people_in_lift == capacity:
        return True
    else: return False

def is_floor_empty(floor_request):
    if len(floor_request) == 0:
        return True
    else: return False

def requests_completed(all_requests):
    floors_completed = 0
    for requests in all_requests:
        if len(requests) == 0:
            floors_completed += 1
    if floors_completed == top_floor:
        return True
    else: return False
    
def change_direction(current_floor, Up):
    if (current_floor == top_floor - 1) and Up == True: return True
    elif (current_floor == 0) and Up == False: return True
    else: return False

def leaving_lift(lift, current_floor):
    people_leaving = []
    for people in lift:
        if people == current_floor + 1:
            people_leaving.append(people)
    for people in people_leaving:
        lift.remove(people)
    return lift

def requests_in_direction_complete(all_requests, current_floor, Up):
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
                if characters.isnumeric():
                    temp_list.append(int(characters))
            amount_of_floors = temp_list[0]
            capacity = temp_list[1]
        elif ":" in list(line):
            list_type_of_requests = list(line)
            temp_list2 = []
            index = list_type_of_requests.index(":")
            if index == 1:
                temp_list2.append(list_type_of_requests[0])
                floor = int(temp_list2[0])
                if floor > top_floor:
                    top_floor = floor
                for x in range(0, 2):
                    list_type_of_requests.pop(0)
            elif index > 1:
                for x in range(0, index):
                    temp_list2.append(list_type_of_requests[0])
                    list_type_of_requests.pop(0)
                    if x == index - 1:
                        list_type_of_requests.pop(0)
                        floor = int("".join(temp_list2))
                        if floor > top_floor:
                            top_floor = floor
            making_list_of_requests(list_type_of_requests)

def upLift(lift, all_requests, current_floor, completed, Up):
    Up = True
    for floor in range(current_floor, top_floor):
        leaving_lift(lift, current_floor)
        if requests_completed(all_requests) == True and len(lift) == 0:
            None # need to add time here ( return time)
        else:
            people_added = []
            for people in all_requests[floor]:
                if isLiftFull(len(lift)) == False:
                    lift.append(people)
                    people_added.append(people)
                elif isLiftFull(len(lift)) == True: break
            for people in people_added:
                all_requests[floor].remove(people)
        if requests_in_direction_complete(all_requests, current_floor, Up) == True:
            if requests_completed(all_requests) == True and len(lift) > 0:
                continue
            elif requests_completed(all_requests) == True and len(lift) == 0:
                return lift, all_requests, current_floor, completed, Up
        if change_direction(current_floor, Up) == True:
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
    if requests_completed(all_requests) == True and len(lift) == 0:
        completed = True
        return lift, all_requests, current_floor, completed, Up
    else: return lift, all_requests, current_floor, completed, Up

def downLift(lift, all_requests, current_floor, completed, Up):
    Up = False
    for floor in range(current_floor, -1, -1):
        leaving_lift(lift, current_floor)
        if requests_completed(all_requests) == True and len(lift) == 0:
            None # need to add time here (return time)
        else:
            people_added = []
            for people in all_requests[floor]:
                if isLiftFull(len(lift)) == False:
                    lift.append(people)
                    people_added.append(people)
                elif isLiftFull(len(lift)) == True: break
            for people in people_added:
                all_requests[floor].remove(people)
        if requests_in_direction_complete(all_requests, current_floor, Up) == True:
            if requests_completed(all_requests) == True and len(lift) > 0:
                continue
            elif requests_completed(all_requests) == True and len(lift) == 0: 
                return lift, all_requests, current_floor, completed, Up
        if change_direction(current_floor, Up) == True:
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
    if requests_completed(all_requests) == True and len(lift) == 0:
        completed = True
        return lift, all_requests, current_floor, completed, Up
    else: return lift, all_requests, current_floor, completed, Up

n = 0

while completed == False:
    if n == 100:
        completed = True
    n += 1
    if Up == True:
        lift, all_requests, current_floor, completed, Up = upLift(lift, all_requests, current_floor, completed, Up)
    elif Up == False:
        lift, all_requests, current_floor, completed, Up = downLift(lift, all_requests, current_floor, completed, Up)
