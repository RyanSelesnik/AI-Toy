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
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        # play memory game
        prev_bot_turn = memory_game_utils.emptyTempFile()
        user_turn = tracker.get_slot("items")
        num_rounds=0

        if memory_game_utils.isValid(prev_bot_turn, user_turn):
            new_bot_turn = memory_game_utils.proceedValidTurn(user_turn)
            num_rounds+=1
            dispatcher.utter_message(text=f"I went to the market and I bought {new_bot_turn}")
            return []
        else:
            dispatcher.utter_message(text=f"Well done! You made it to {num_rounds} rounds this time! Keep playing to improve your skills.")
            open('./data/past_events.txt', 'w').close()
            return []


