import json
from typing import Dict, List

from expense_tracker.base import Category, Currency, Expense


class Database:
    def __init__(self, path):
        self.path = path

    def connect(self) -> Dict[str, Expense]:
        print("Connecting to database...")

        with open(self.path) as database_file:
            raw_expenses: List[Dict[str, str]] = json.load(database_file)

        expenses = {}
        curr_pk = 1
        for expense in raw_expenses:
            expenses[curr_pk] = Expense(
                pk=curr_pk,
                name=expense["name"],
                date=expense["date"],
                amount=expense["amount"],
                description=expense["description"],
                active=expense["active"],
                category=Category.get_or_create(expense["category"]),
                currency=Currency(pk=expense["currency_id"]),
            )

            curr_pk += 1

        return expenses
