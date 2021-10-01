from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

from connectivity import DataUpdate, SaveChat

class ActionContactConfirm(Action):

    def name(self) -> Text:
        return "action_contact_confirm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        DataUpdate(tracker.get_slot("name"),tracker.get_slot("contact_details"),tracker.get_slot("subject"))
        response = "Thank you for reaching us, {}! We'll reply to the {}.⏱️ \nWe usually reply within 24 business hours so stay tuned!".format(tracker.get_slot("name"), tracker.get_slot("contact_details"))
        dispatcher.utter_message(response)
        
        # save conversation in csv file
        conversation = tracker.events
        SaveChat(conversation)

        return [AllSlotsReset()]

class ActionSaveConversation(Action):
    def name(self) -> Text:
        return "action_save_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conversation = tracker.events
        # print(conversation) # to print raw conversation
        SaveChat(conversation)
        dispatcher.utter_message(text="All chat saved.")
        return []