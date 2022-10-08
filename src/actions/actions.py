from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List
import re


class ActionPlayFizzBuzz(Action):

    def name(self) -> Text:
        return "action_play_fizz_buzz"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # TODO: currently only works with numerical inputs, extend to strings like 'one', 'two' etc
        # TODO: handle misspelt words like 'fazz'
        # TODO: handle when user enters 'fizz' or 'buzz' etc. => need conversation history
        # TODO: Win or lose
        # Choose divisors

        divisor_1 = 3
        divisor_2 = 5

        # fb_game = []
        # for i in range(1, 99):
        print(tracker.events)

        fb_entry = tracker.latest_message['entities'][0]['value']
        # Entity can other be a number or the words 'fizz' 'buzz' etc.
        fb_entity = tracker.latest_message['entities'][0]['entity']

        output = ""
        if fb_entity == 'fizz_buzz_entry':
            print(tracker.events[-5].tex)
            bot_utterance = int(tracker.events[-5].get('text'))
            bot_utterance += 2
            dispatcher.utter_message(text=bot_utterance)
            return
        fb_entry = int(fb_entry)
        #  Increment entry for the bots turn
        fb_entry += 1

        if fb_entry % divisor_1 == 0:
            output += "fizz"
        if fb_entry % divisor_2 == 0:
            output += "buzz"

        if output == "":
            output = str(fb_entry)

        dispatcher.utter_message(text=output)

        return []
