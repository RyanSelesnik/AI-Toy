# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from random import seed
import random
class ActionPlayMemoryGame(Action):
   
    def name(self) -> Text:
        return "action_play_memory_game"
 
    def computer_turn(self):
        computer_turn=[]
        with open('data/memory_game/items.txt', "r") as f:
            list_of_objects = f.read().splitlines()
        computer_turn=list_of_objects[random.randint(0,len(list_of_objects))-1]
        return(computer_turn)
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        # play memory game
        user_turn = tracker.get_slot("items")
        print(f'user: {user_turn}')
        comp_turn = self.computer_turn()
        print(f'computer: {comp_turn}')
        user_turn.append(comp_turn)
        print(f'full list: {user_turn}')
        # dispatcher.utter_message(text=f"I went to the market and I bought {user_turn}")
        return []


