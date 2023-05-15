from readchar import readchar
import time
import numpy as np
import threading
import sys


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
    inpt = int(input(":"))
    if inpt == 1:
        tprint("It was a trap! You died!")
        quit()
    else:
        tprint("You continue looking for the city.")
        tprint("You are tired, do you continue looking for the city or leave?\n1. Continue\n2. Leave")
        inpt = int(input("\n:"))
        if inpt == 1:
            pass
        else:
            tprint("You leave the cave and go home.")
            tprint("You Loose!")
            quit()
def endroom():
    print("End Room")
    pass
# thread3.start()
# thread4.start()