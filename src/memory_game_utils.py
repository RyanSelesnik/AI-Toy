import random
from random import seed
import copy
from rasa_sdk.executor import CollectingDispatcher
PATH_TO_PREV_BOT_TURN = './past_events.txt'

def readInTempFile():
    with open(PATH_TO_PREV_BOT_TURN, 'r') as f:
        prev_bot_turn = [line.rstrip('\n') for line in f]
    return prev_bot_turn
        
def computer_turn(user_turn):
    with open('./data/memory_game/items.txt', "r") as f:
        list_of_objects = f.read().splitlines()
        for item in list_of_objects:
            if item in user_turn:
                list_of_objects.remove(item) 
    computer_turn=list_of_objects[random.randint(0,len(list_of_objects))-1]
    return computer_turn

def isValid(prev_bot_turn, curr_user_turn, dispatcher: CollectingDispatcher):
    if (len(prev_bot_turn) == 0):
        #user's first move is always valid
        return True
    elif curr_user_turn[:-1] != prev_bot_turn:
        errors = []
        #if user turn differs from the previous turn before the last element in the list, they lose
        for i in range(0, len(prev_bot_turn)):
            if curr_user_turn[i] != prev_bot_turn[i]:
                errors.append(prev_bot_turn[i])
        dispatcher.utter_message(text=f"Ahh man. You left out the item {errors}. Keep playing to improve your skills.")
        return False
    elif curr_user_turn[-1] in prev_bot_turn:
        #if user adds already existing list item, they lose
        dispatcher.utter_message(text=f"Oops, you have already bought that item. You did so well though! Come back soon since practice makes perfect!")
        return False
    else:
        #if the game has not just begun, but bot's previous turn matches user's current turn, user is still in play
        return True

def proceedValidTurn(user_turn):
    open(PATH_TO_PREV_BOT_TURN, 'w').close()
    bot_addition = computer_turn(user_turn)
    new_bot_turn = user_turn.copy()
    new_bot_turn.append(bot_addition)
    with open(PATH_TO_PREV_BOT_TURN, 'w') as f:
        for entity in new_bot_turn:
            f.write(entity + '\n')
    return new_bot_turn
        