
from memory_game_utils import PATH_TO_PREV_BOT_TURN, isValid, computer_turn, proceedValidTurn, readInTempFile
import copy
from random import seed
from urllib import response
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List
import os
from math_game_utils import map_entities_to_ints, list_is_valid, reset_game

PATH_TO_FILE = './latest_number.txt'

# This is a simple example for a custom action which utters "Hello World!"


# import random
# import memory_game_utils


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
            dispatcher.utter_message(
                text=f"I went to the market and I bought {new_bot_turn}")
            return []
        else:
            dispatcher.utter_message(
                text=f"You made it to {len(prev_bot_turn)-1} rounds this time!")
            open(PATH_TO_PREV_BOT_TURN, 'w').close()
            return []


class MathGameCount(Action):
    """
    Plays the counting game
    """

    def name(self) -> Text:
        return "action_math_game_count"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get current entities in user utterance
        entities = tracker.get_slot("math_game_number")

        list_of_ints = map_entities_to_ints(entities)

        # A list is valid depneds on the current list and past list (stored in PATH_TO_FILE)
        if list_is_valid(list_of_ints, PATH_TO_FILE):
            dispatcher.utter_message(text="Woah, Nice! Carry on")
        else:
            dispatcher.utter_message(text="You lose")
            reset_game(PATH_TO_FILE)

        return []


class CreateMathGameFile(Action):

    def name(self) -> Text:
        return "action_create_math_game_file"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        reset_game(PATH_TO_FILE)
