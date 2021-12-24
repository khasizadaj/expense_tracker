import json
from typing import Dict

from expense_tracker.base import Category, Currency, Expense


class Database:
    def __init__(self, path):
        self.path = path

    def connect(self) -> Dict[str, Expense]:
        print("Connecting to database...")

        with open(self.path) as database_file:
            raw_expenses = json.load(database_file)

        expenses = {}
        for expense_id, expense in raw_expenses.items():
            expenses[expense_id] = Expense(
                id=expense["id"],
                name=expense["name"],
                date=expense["date"],
                amount=expense["amount"],
                description=expense["description"],
                active=expense["active"],
                category=Category(),
                currency=Currency(id=expense["currency_id"]),
            )

        return expenses
