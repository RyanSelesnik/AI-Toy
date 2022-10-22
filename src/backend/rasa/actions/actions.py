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
import os
# import random
import copy
# import memory_game_utils
from memory_game_utils import PATH_TO_PREV_BOT_TURN, isValid, computer_turn, proceedValidTurn, readInTempFile
class CreateMemoryGameFile(Action):

    def name(self) -> Text:
        return "action_create_memory_game_file"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            os.system(f"rm {PATH_TO_PREV_BOT_TURN}")
        except FileNotFoundError as e:
            print(e)
        os.system(f"touch {PATH_TO_PREV_BOT_TURN}")
        
class ActionPlayMemoryGame(Action):
   
    def name(self) -> Text:
        return "action_play_memory_game"
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        # play memory game
        user_turn = tracker.get_slot("items")
        prev_bot_turn = readInTempFile()

        if isValid(prev_bot_turn, user_turn, dispatcher):
            new_bot_turn = proceedValidTurn(user_turn)
            dispatcher.utter_message(text=f"I went to the market and I bought {new_bot_turn}")
            return []
        else:
            dispatcher.utter_message(text=f"You made it to {len(prev_bot_turn)-1} rounds this time!")
            open(PATH_TO_PREV_BOT_TURN, 'w').close()
            return []
