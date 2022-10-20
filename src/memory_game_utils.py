import random
from random import seed
import copy

def emptyTempFile():
    with open('./data/past_events.txt', 'r') as f:
        prev_bot_turn = [line.rstrip('\n') for line in f]
    return prev_bot_turn
        
def computer_turn():
    computer_turn=[]
    with open('data/memory_game/items.txt', "r") as f:
        list_of_objects = f.read().splitlines()
    computer_turn=list_of_objects[random.randint(0,len(list_of_objects))-1]
    print(type(computer_turn))
    return computer_turn

def isValid(prev_bot_turn, curr_user_turn):
    if (len(prev_bot_turn)==0):
        #user's first move is always valid
        return True
    elif curr_user_turn[:-1]!=prev_bot_turn:
            #if user turn differs from the previous turn before the last element in the list, they lose
        return False
    else:
            #if the game has not just begun, but bot's previous turn matches user's current turn, user is still in play
        return True

def proceedValidTurn(user_turn):
    open('./data/past_events.txt', 'w').close()
    bot_addition = computer_turn()
    new_bot_turn = user_turn.copy()
    new_bot_turn.append(bot_addition)
    with open('./data/past_events.txt', 'w') as f:
        for entity in new_bot_turn:
            f.write(entity + '\n')
    return new_bot_turn
        