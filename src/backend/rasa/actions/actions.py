
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List
import os
from math_game_utils import map_entities_to_ints, list_is_valid

PATH_TO_PREV_NUMBER = './latest_number.txt'


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

        if list_is_valid(list_of_ints, PATH_TO_PREV_NUMBER):
            dispatcher.utter_message(text="Woah, Nice! Carry on")
        else:
            dispatcher.utter_message(text="You lose")

        return []


class CreateMathGameFile(Action):

    def name(self) -> Text:
        return "action_create_math_game_file"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            os.system(f"rm {PATH_TO_PREV_NUMBER}")
        except FileNotFoundError:
            print("file does not exist")

        os.system(f"touch {PATH_TO_PREV_NUMBER}")
