from typing import Dict, Optional
from expense_tracker.base import Category, Currency, Expense, ExpensesFactory


class CreateExpensesFactory(ExpensesFactory):
    def execute(self, flags: Dict[str, str]) -> Expense:
        expense_details = self.get_expense_details()
        expense = self.save(expense_details)
        return expense

    def get_expense_details(self) -> Dict[str, str]:
        # TODO check if optional or required
        flags = {
            "--id": "5",
            "--name": "Phone",
            "--date": "25.12.21",
            "--amount": "890",
            "--description": "Killing hunger",
            "--category": Category("technology"),
            "--currency_id": "4",
        }

        return flags

    def save(self, flags: Dict[str, str]) -> Dict[str, Expense]:
        # "--id": auto generated
        # "--active" : always true at the beginning
        category = Category.get_or_create(name=flags.get("--category"))
        currency = Currency(pk=flags.get("--currency_id"))
        expense = Expense(
            pk=flags.get("--id"),
            name=flags.get("--name"),
            date=flags.get("--date"),
            amount=flags.get("--amount"),
            description=flags.get("--description"),
            active=True,
            category=category,
            currency=currency,
        )

        return {expense.pk: expense}
