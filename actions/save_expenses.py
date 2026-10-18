
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.db import Expense, add_expense


class SaveExpense(Action):
    def name(self) -> str:
        return "save_expense"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any],
    ) -> List[Dict[Text, Any]]:

        amount = tracker.get_slot("expense_amount")
        category = tracker.get_slot("expense_category")
        description = tracker.get_slot("expense_description")

        if amount is None or category is None:
            dispatcher.utter_message(
                text="Please provide an expense amount and category."
            )
            return [SlotSet("return_value", "data_not_present")]

        try:
            value = Decimal(str(amount))
            if not value.is_finite() or value <= 0:
                raise InvalidOperation
        except (InvalidOperation, ValueError):
            dispatcher.utter_message(
                text="Please provide a valid positive expense amount."
            )
            return [SlotSet("return_value", "invalid_amount")]

        expense = Expense(
            description=str(description or category),
            amount=str(value),
            category=str(category),
            currency="USD",
        )

        add_expense(tracker.sender_id, expense)

        dispatcher.utter_message(
            text=f"Expense saved: ${value:.2f} for {category}."
        )

        return [SlotSet("return_value", "success")]
