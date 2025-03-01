import time

def making_list_of_requests(list_type_of_requests):
    temp_list = []
    if len(list_type_of_requests) > 1:
        list_type_of_requests = "".join(list_type_of_requests)
        list_type_of_requests = list_type_of_requests.strip()  # remove any extra newlines or spaces
        list_type_of_requests = list_type_of_requests.replace(" ", "").split(",")  # split by commas

        for request in list_type_of_requests:
            if request:  # Check if the request is not an empty string
                try:
                    temp_list.append(int(request))  # convert the request to an integer and add it to the list
                except ValueError:
                    continue  # If there's an invalid value, skip it
        all_requests.append(temp_list)  # adds the processed requests to the all_requests list
    elif len(list_type_of_requests) == 1:
        list_type_of_requests.pop(0)  # Remove the floor with no requests
        all_requests.append(list_type_of_requests)
    elif len(list_type_of_requests) == 0:
        all_requests.append(list_type_of_requests)


def isLiftFull(people_in_lift):
    if people_in_lift == capacity:
        return True
    else:
        return False


def is_floor_empty(floor_request):
    if len(floor_request) == 0:
        return True
    else:
        return False


def requests_completed(all_requests):  # checks to see if there are no more requests across all floors
    floors_completed = 0
    for requests in all_requests:
        if len(requests) == 0:
            floors_completed += 1
    if floors_completed == top_floor:
        print("All requests completed.")  # Debugging: Check if all requests are completed
        return True
    else:
        return False


def change_direction(current_floor, Up):  # checks to see if lift has hit bottom or top floor
    if (current_floor == top_floor - 1) and Up == True:
        print("Reached top floor. Changing direction to down.")  # Debugging
        return True
    elif (current_floor == 0) and Up == False:
        print("Reached bottom floor. Changing direction to up.")  # Debugging
        return True
    else:
        return False


def leaving_lift(lift, current_floor):  # takes people out the lift if their at the floor requested
    people_leaving = []
    for people in lift:
        if people == current_floor + 1:
            people_leaving.append(people)
    for people in people_leaving:
        lift.remove(people)
    return lift


def requests_in_direction_complete(all_requests, current_floor, Up):  # checks if all requests in direction lift is travelling are completed
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
    else:
        return False


all_requests = []
lift = []
line_in_file = 0
top_floor = 0
current_floor = 0
Up = True
completed = False

# Simulating reading from file (replace with actual file reading as needed)
# The 'input.txt' file should contain the requested format.
input_data = [
    "5 3\n",
    "0: 1, 2, 3\n",
    "1: 4\n",
    "2: 5\n",
    "3: \n",
    "4: 5\n",
    "5: 0\n"
]

# Read input from file (Simulated as list of strings above)
for line in input_data:
    temp_list = []
    line_in_file += 1
    if line_in_file == 1:
        for characters in list(line):
            if characters.isnumeric():  # gets rid of all the characters in the line except for numbers
                temp_list.append(int(characters))  # adds them as integers to a different list
        amount_of_floors = temp_list[0]
        capacity = temp_list[1]
    elif ":" in list(line):  # checks for the lines of text with the requests
        list_type_of_requests = list(line)
        temp_list2 = []
        index = list_type_of_requests.index(":")
        if index == 1:  # checks if it is a single digit floor
            temp_list2.append(list_type_of_requests[0])  # adds floor num to a list
            floor = int(temp_list2[0])
            if floor > top_floor:
                top_floor = floor  # sees which floor is highest and makes it top floor
            for x in range(0, 2):
                list_type_of_requests.pop(0)  # gets rid of the n: from line
        elif index > 1:  # checks if floor has more than a single digit
            for x in range(0, index):  # goes through numbers before :
                temp_list2.append(list_type_of_requests[0])
                list_type_of_requests.pop(0)  # removes numbers before :
                if x == index - 1:
                    list_type_of_requests.pop(0)  # removes the :
                    floor = int("".join(temp_list2))  # joins the temp list together to make the floor number
                    if floor > top_floor:
                        top_floor = floor
        making_list_of_requests(list_type_of_requests)  # processes requests


def upLift(lift, all_requests, current_floor, completed=False, Up=True):  # lift going up
    for floor in range(current_floor, top_floor):  # goes through all floors between current floor and top floor
        print(f"Processing floor {floor}...")  # Debugging
        leaving_lift(lift, current_floor)  # takes people out lift if the floor is the one they requested
        if requests_completed(all_requests) == True and len(lift) == 0:
            completed = True
            break
        # Add people to lift if space allows
        people_added = []
        for people in all_requests[floor]:
            if not isLiftFull(len(lift)):
                lift.append(people)
                people_added.append(people)
            elif isLiftFull(len(lift)):
                break  # Stop adding people if the lift is full

        for people in people_added:
            all_requests[floor].remove(people)

        if requests_in_direction_complete(all_requests, current_floor, Up):
            if requests_completed(all_requests) and len(lift) == 0:
                completed = True
                break

        if change_direction(current_floor, Up):
            Up = False
            break
        else:
            current_floor += 1

    return lift, all_requests, current_floor, completed, Up


def downLift(lift, all_requests, current_floor, completed=False, Up=True):
    Up = False
    for floor in range(current_floor, -1, -1):  # moves from current down to 0 floor
        print(f"Processing floor {floor}...")  # Debugging
        leaving_lift(lift, current_floor)  # takes people out lift if the floor is the one they requested
        if requests_completed(all_requests) == True and len(lift) == 0:  # checks if all requests have been completed
            completed = True
            break
        # Add people to lift if space allows
        people_added = []
        for people in all_requests[floor]:
            if not isLiftFull(len(lift)):
                lift.append(people)
                people_added.append(people)
            elif isLiftFull(len(lift)):
                break  # Stop adding people if the lift is full

        for people in people_added:
            all_requests[floor].remove(people)

        if requests_in_direction_complete(all_requests, current_floor, Up):
            if requests_completed(all_requests) and len(lift) == 0:
                completed = True
                break

        if change_direction(current_floor, Up):
            Up = True
            break
        else:
            current_floor -= 1

    return lift, all_requests, current_floor, completed, Up


def Lift(lift, all_requests, current_floor, completed=False, Up=True):
    start_time = time.time()  # Start the timer to calculate time taken for the operation
    
    # Initialize all_requests with empty lists for each floor (ensure it has enough floors)
    if len(all_requests) < top_floor:
        all_requests.extend([[]] * (top_floor - len(all_requests)))  # Extend with empty lists for missing floors

    while completed == False:
        print(f"Current floor: {current_floor}, Lift: {lift}, Direction: {'Up' if Up else 'Down'}")  # Debugging
        if Up == True:
            lift, all_requests, current_floor, completed, Up = upLift(lift, all_requests, current_floor, completed, Up)
        elif Up == False:
            lift, all_requests, current_floor, completed, Up = downLift(lift, all_requests, current_floor, completed, Up)

        # Check completion condition
        if requests_completed(all_requests) and len(lift) == 0:
            completed = True  # Once all requests are completed, mark the system as done
            print("Lift operation completed.")  # Debugging
            break

    end_time = time.time()
    return (end_time - start_time) * 1000  # Return time taken in milliseconds
