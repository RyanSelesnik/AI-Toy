import random
from random import seed
import copy

def computer_turn():
    computer_turn=[]
    with open('data/memory_game/items.txt', "r") as f:
        list_of_objects = f.read().splitlines()
    computer_turn=list_of_objects[random.randint(0,len(list_of_objects))-1]
    return computer_turn

def isValid(prev_bot_turn, curr_user_turn):
    if (len(prev_bot_turn)==0):
        #user's first move is always valid
        return True
    for i in range (0,len(prev_bot_turn)):
        if curr_user_turn[i]!=prev_bot_turn[i]:
            #if user turn differs from the previous turn before the last element in the list, they lose
            return False
        else:
            #if the game has not just begun, but bot's previous turn matches user's current turn, user is still in play
            return True
        