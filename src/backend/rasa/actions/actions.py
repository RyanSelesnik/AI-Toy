from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List


class MathGameCount(Action):

    def name(self) -> Text:
        return "action_math_game_count"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        test = tracker.get_latest_entity_values()
        print(test)

        dispatcher.utter_message(text="Hello World!")

        return []
