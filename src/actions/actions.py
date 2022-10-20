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
# import random
import copy
import memory_game_utils
class ActionPlayMemoryGame(Action):
   
    def name(self) -> Text:
        return "action_play_memory_game"
 
    def get_computer_turn(self):
        computer_turn = memory_game_utils.computer_turn()
        return computer_turn
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        # play memory game
        with open('./data/past_events.txt', 'r') as f:
            prev_bot_turn = [line.rstrip('\n') for line in f]

        user_turn = tracker.get_slot("items")
        num_rounds=0

        if memory_game_utils.isValid(prev_bot_turn, user_turn):
            num_rounds+=1
            open('./data/past_events.txt', 'w').close()
            bot_addition = self.get_computer_turn()
            new_bot_turn = user_turn.copy()
            new_bot_turn.append(bot_addition)
            with open('./data/past_events.txt', 'w') as f:
                for entity in new_bot_turn:
                    f.write(entity + '\n')
            dispatcher.utter_message(text=f"I went to the market and I bought {new_bot_turn}")
            return []
        else:
            dispatcher.utter_message(text=f"Well done! You made it to {'??'} rounds this time! Keep playing to improve your skills.")
            open('./data/past_events.txt', 'w').close()
            return []


