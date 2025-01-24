import random

n=10
elevator = [0,-1] #0-n
floors = {}
for i in range(0, n):
    floors[str(i)] = [random.randint(0, n-1) for i in range(0, random.randint(0, 3))]


flag = 1
while True:
    print("\033c")
    print(floors)
    print("You are at floor ", elevator[0])
    if elevator[1] != -1:
        print("Target Floor: ", elevator[1])
    else:
        print("No target floor")
        if len(floors[str(elevator[0])]) > 0:
            elevator[1] = floors[str(elevator[0])].pop()
    
    if elevator[0] == elevator[1]:
        print("You have reached the target floor")
        elevator[1] = -1
        
    if flag:
        elevator[0] += 1
        if elevator[0] == n-1:
            flag = 0
    else:
        elevator[0] -= 1
        if elevator[0] == 0:
            flag = 1
    input("Press Enter to continue...")