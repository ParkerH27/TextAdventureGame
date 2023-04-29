from readchar import readchar
import time
import numpy as np
import threading
import sys



global x
global y
global playerchar
global ox
global oy
global hearts
hearts = 3
global screen
global grid
global smgrid
global toggletrap
global bgcolor
bgcolor = "\033[92m"



def clear():
    print("\033[H\033[2J", end="", flush=True)

width = 12





with open("level1.txt", "r") as f:
    lines = f.readlines()


num_rows = len(lines)
num_cols = max([len(line.strip()) for line in lines])


lines = [line.strip().ljust(num_cols) for line in lines]


arr = np.full((num_rows, num_cols), ".")



for row in range(num_rows):
    for col in range(num_cols):
        arr[row][col] = lines[row][col]

arr = np.char.replace(arr, ".", " ")
global heartcolor
heartcolor = "\033[91m♥\033[0m"+ bgcolor
arr = np.char.replace(arr, "♥", heartcolor)

heartstring = ""
def heartcount(hearts):
    heartstring = ""
    for i in range(hearts):
        heartstring += heartcolor
    return heartstring


x = 1

y = 1

playerchar = " "

ox = 0

oy = 0
screen = ""
grid = np.array(arr, dtype=object)
toggletrap = 0


def t1():
    global x
    global y
    global playerchar
    global ox
    global oy
    global hearts
    global screen
    global grid
    global smgrid
    global toggletrap
    global heartcolor
    global bgcolor
    a = True
    heartstring = heartcount(hearts)
    screen = heartstring
    while a == True:
        if grid[y][x] == heartcolor:
            arr[y][x] = " "
            hearts += 1
            heartstring = heartcount(hearts)
            screen = heartstring
        if grid[y][x] != " " and grid[y][x] != heartcolor:
            x = ox
            y = oy
            oy = 0
            ox = 0
        else:
            clear()
            grid[y][x] = '\033[96m' + playerchar +'\033[0m' + bgcolor
            grid[oy][ox] = arr[oy][ox]
            str = bgcolor
            nx = x - width
            ny = y - width
            px = x + width
            py = y + width
            if nx < 0:
                nx = 0
            if ny < 0:
                ny = 0
            if px > num_cols:
                px = num_cols
            if py > num_cols:
                py = num_cols
            str += "╔" + ("═" * (px-abs(nx))) + "╗"+"\n"
            smgrid = grid[ny:py, nx:px]
            for i in smgrid:
                str += "║"
                str += "".join(i)
                str += "║"
                str += "\n"
            str += "╚" + ("═" * (px-abs(nx))) + "╝"
            str += "\n"
            str += screen
            str += "\n"
            print(str)
        ox = x
        oy = y
        time.sleep(0.05)
def t2():
    global x
    global y
    global playerchar
    global ox
    global oy
    global hearts
    global screen
    global grid
    global smgrid
    global toggletrap
    while True:
        rc = readchar()
        if rc == 'w':
            y-=1
            playerchar = "▲"
        elif rc == 'a':
            x-=1
            playerchar = "◀"
        elif rc == 's':
            y+=1
            playerchar = "▼"
        elif rc == 'd':
            x+=1
            playerchar = "▶"
        elif rc == 'z':
            x-=1
            y+=1
            playerchar = "◣"
        elif rc == 'e':
            x+=1
            y-=1
            playerchar = "◥"
        elif rc == 'q':
            x-=1
            y-=1
            playerchar = "◤"
        elif rc == 'c':
            x+=1
            y+=1
            playerchar = "◢"
        else:
            pass
        time.sleep(0.05)

# def t3():
#     global x
#     global y
#     global playerchar
#     global ox
#     global oy
#     global hearts
#     global screen
#     global grid
#     global smgrid
#     global toggletrap
#     while True:
#         pass

# def t4():
#     global toggletrap
#     while True:
#         pass


def tprint(text):
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.08)

print("\n")
tprint("Establishing")
time.sleep(0.4)
print(".", end="")
time.sleep(0.4)
print(".", end="")
time.sleep(0.4)
print(".")
time.sleep(0.9)
tprint("--------------")
time.sleep(0.2)
clear()

time.sleep(3)

thread1 = threading.Thread(target=t1)
thread2 = threading.Thread(target=t2)
# thread3 = threading.Thread(target=t3)
# thread4 = threading.Thread(target=t4)
thread1.start()
thread2.start()
# thread3.start()
# thread4.start()