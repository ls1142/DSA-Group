import random, time


start = time.time()


n=10
elevator = [0,-1] #0-n
floors = {}
p = 0
capacity = 1




for i in range(0, n):
    floors[str(i)] = [random.randint(0, n-1) for i in range(0, random.randint(0, 3))]
    p+=len(floors[str(i)])


def checkIfEmpty(floors):
    flag = True
    for i in range(0,n):
        if floors[str(i)] != []:
            flag = False

    return flag



running = True
flag = 1
while running:
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
    
    if checkIfEmpty(floors):
        running = False#


end = time.time()
print(f"runtime is: {end-start:.6f}s")
print(f"people: {p}")
