from rasa_sdk.events import SlotSet
from typing import Dict, Text, Any, List, Union
from rasa_sdk import Tracker, Action,FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import AllSlotsReset, Restarted



class ActionHandleFaq(Action):

    def name(self):
        return "action_handle_faq"

    def run(self, dispatcher, tracker, domain):
        admitted = tracker.get_slot('admitted')
        if admitted:
            return [SlotSet("admitted", admitted)]
        
        degree = tracker.get_slot('degree')
        if degree:
            return [SlotSet("degree", degree)]
        return []


class ActionRestartAndResetSlots(Action):
    def name(self) -> str:
        return "action_restart_and_reset_slots"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Restarting the chat...")
        return [AllSlotsReset(), Restarted()]
    
 

class ActionDeactivateForm(Action):
    def name(self) -> str:
        return "action_deactivate_form"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="The form has been deactivated.")
        return []
       

class ValidateRestaurantForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_polito_form"

    @staticmethod
    def degree_db() -> List[Text]:
        """Database of supported degrees"""
        return ["bachelor", "master"]

    def validate_degree(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate degree value."""
        if slot_value.lower() in self.degree_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"degree": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"degree": None}

    def validate_admitted(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate admitted value."""
        if slot_value.lower() in ('yes','not yet'):
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"admitted": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"admitted": None}
   
    def validate_language(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate language value."""
        if slot_value.lower() in ('italian','non italian'):
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"language": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"language": None}

    