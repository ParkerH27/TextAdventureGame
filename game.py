import sys
import threading
import time

import numpy as np
from readchar import readchar

global x
global y
global playerchar
global ox
global oy
global px
global py
global nx
global ny
global items
global screen
global grid
global smgrid
global toggletrap
global bgcolor
global killthread
global game
global num_rows
global num_cols
global heartcolor
global watercolor
global keycolor
global keystring
global heartstring
global arr
global room
px, py, nx, ny = 0, 0, 0, 0
items = [3, 0]
bgcolor = "\033[92m"
killthread = False
game = True
width = 12


def clear():
    print("\033[H\033[2J", end="", flush=True)


def open_level(leveltxt):
    global x
    global y
    global playerchar
    global ox
    global oy
    global px
    global py
    global nx
    global ny
    global items
    global screen
    global grid
    global smgrid
    global toggletrap
    global bgcolor
    global killthread
    global game
    global num_rows
    global num_cols
    global heartcolor
    global watercolor
    global keycolor
    global keystring
    global heartstring
    global arr
    global level
    with open(leveltxt, "r") as f:
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
    heartcolor = "\033[91m♥\033[0m" + bgcolor
    arr = np.char.replace(arr, "♥", heartcolor)
    keycolor = "\033[93m╼\033[0m" + bgcolor
    arr = np.char.replace(arr, "╼", keycolor)
    watercolor = "\033[94m~\033[0m" + bgcolor
    arr = np.char.replace(arr, "~", watercolor)

    heartstring = ""
    keystring = ""
    x = 1

    y = 1

    playerchar = " "

    ox = 0

    oy = 0
    screen = ""
    grid = np.array(arr, dtype=object)
    toggletrap = 0


def heartcount(hearts):
    heartstring = ""
    for i in range(hearts):
        heartstring += heartcolor
    return heartstring


def keycount(keys):
    keystring = ""
    for i in range(keys):
        keystring += keycolor
    return keystring


def scrprt(width):
    global screen
    screen = heartstring + " " * (((width) + 2) - (items[0] + items[1])) + keystring


def cave_explo():
    global x
    global y
    global playerchar
    global ox
    global oy
    global items
    global screen
    global grid
    global smgrid
    global toggletrap
    global heartcolor
    global watercolor
    global bgcolor
    global keycolor
    global num_cols
    global num_rows
    global keystring
    global heartstring
    global px
    global py
    global nx
    global ny
    global killthread
    global game
    global arr
    global level
    heartstring = heartcount(items[0])
    keystring = keycount(items[1])
    scrprt(px - abs(nx))
    while killthread == False:
        if items[0] == 0:
            print("You died!")
            sys.exit()
        if grid[y][x] == heartcolor:
            arr[y][x] = " "
            items[0] += 1
            heartstring = heartcount(items[0])
            scrprt(px - abs(nx))
        elif grid[y][x] == keycolor:
            arr[y][x] = " "
            items[1] += 1
            keystring = keycount(items[1])
            scrprt(px - abs(nx))
        elif grid[y][x] == "☰":
            arr[y][x] = " "
            tprint("You found a note!\n")
            tprint("It reads:\n 5/6/1926\n I found a river today near the Library. I think I will follow it tomorrow.\n")
            if "1" in input("Do you find and follow the river?\n1. Yes\n2. No\n>:"):
                clear()
                print("You follow the river and find a cave.")
                endroom()
        elif grid[y][x] == watercolor:
            game = False
            print("")
            print("")
            if "1" in input("Follow the underground river?\n1. Yes\n2. No\n>:"):
                clear()
                print("You follow the river and find a cave.")
                endroom()
            else:
                game = True
        elif grid[y][x] == "∆":
            items[0] -= 1
            heartstring = heartcount(items[0])
            scrprt(px - abs(nx))
        elif grid[y][x] == "⊡":
            if items[1] > 0:
                items[1] -= 1
                scrprt(px - abs(nx))
                if level == 1:
                    key()
                    game = True
            if level == 2:
                end()

        scrprt(px - abs(nx))
        if grid[y][x] != " " and grid[y][x] != heartcolor and grid[y][x] != keycolor and grid[y][x] != "∆":
            x = ox
            y = oy
            oy = 0
            ox = 0
        else:
            clear()
            grid[y][x] = "\033[96m" + playerchar + "\033[0m" + bgcolor
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
            str += "╔" + ("═" * (px - abs(nx))) + "╗" + "\n"
            smgrid = grid[ny:py, nx:px]
            for i in smgrid:
                str += "║"
                str += "".join(i)
                str += "║"
                str += "\n"
            str += "╚" + ("═" * (px - abs(nx))) + "╝"
            str += "\n"
            str += screen
            str += "\n"
            print(str)
        ox = x
        oy = y
        time.sleep(0.05)
    clear()
    killthread = True


def tprint(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.08)


def tinput(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    value = input()
    return value


def key():
    global game
    global killthread
    game = False
    killthread = True
    tprint("Door Opened!")
    print()
    tprint("You find treasure behind the door. What do you do?")
    print("")
    tprint("1. Take the treasure.")
    print("")
    tprint("2. Leave the treasure and continue looking for the city.")
    inpt = input("\n:")
    if "1" in str(inpt):
        tprint("It was a trap! You died!")
        sys.exit()
    else:
        tprint("You continue looking for the city.")
        tprint(
            "You are tired, do you continue looking for the city or leave?\n1. Continue\n2. Leave"
        )
        inpt = input("\n:")
        if "1" in str(inpt):
            endroom()
        else:
            tprint("You leave the cave and go home.")
            tprint("You Loose!")
            sys.exit()


def endroom():
    open_level("endcave.txt")
    print("You follow the river and find a deep cave.")
    global game
    global killthread
    global level
    global x
    global y
    game = True
    killthread = False
    x = 1
    y = 1
    level = 2

def control():
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
    global game
    while True:
        print("Control")
        while game:
            print("on")
            rc = readchar()
            if rc == "w":
                y-=1
                playerchar = "▲"
            elif rc == "a":
                x-=1
                playerchar = "◀"
            elif rc == "s":
                y+=1
                playerchar = "▼"
            elif rc == "d":
                x+=1
                playerchar = "▶"
            elif rc == "z":
                x-=1
                y+=1
                playerchar = "◣"
            elif rc == "e":
                x+=1
                y-=1
                playerchar = "◥"
            elif rc == "q":
                x-=1
                y-=1
                playerchar = "◤"
            elif rc == "c":
                x+=1
                y+=1
                playerchar = "◢"
            time.sleep(0.05)
        while not game:
            time.sleep(1)
            pass


def end():
    global game
    global killthread
    global x
    global y
    game = True
    killthread = False
    tprint("Que cutscene!")
    print()
    tprint("You Win!")
    sys.exit()


print("\n")
tprint("Starting")
time.sleep(0.4)
print(".", end="")
time.sleep(0.4)
print(".", end="")
time.sleep(0.4)
print(".")
time.sleep(0.9)
tprint("-----------")
time.sleep(0.2)
clear()

time.sleep(3)
level = 1

ce_thread = threading.Thread(target=cave_explo)
control_thread = threading.Thread(target=control)
# thread3 = threading.Thread(target=t3)
# thread4 = threading.Thread(target=t4)ß
start = False
while not start:
    tprint("Welcome to the game!\n")
    inpt = tinput("use wasd to move\nqezc to move diagonally\nAnswer questions with number keys.(If the answer has no number, the last option will be the default)\n1. I understand\n2. I very clearly do not understand\n:")
    if "1" in str(inpt):
        start = True
tprint("You just found a map to an ancient city in your grandfathers attic.")
inpt = tinput("What do you do?\n1. Follow the map\n2. Stay home and go to sleep\n3. Research about the city\n:")
if "1" in str(inpt):
    open_level("level1.txt")
    tprint("You follow the map and find a cave entrance.")
    tprint("You enter the cave.")
    time.sleep(2)
    ce_thread.start()
    control_thread.start()
elif "2" in str(inpt):
    tprint("You go to sleep")
    tprint("You are The Real Winner!")
    sys.exit()
else:
    open_level("city.txt")
    tprint("You decide to research about the city.")
    ce_thread.start()
    control_thread.start()
