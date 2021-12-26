from typing import Dict, Optional
from expense_tracker.base import Expense, ExpensesFactory


class ReadExpensesFactory(ExpensesFactory):
    def execute(self, flags: Optional[Dict[str, str]]) -> Dict[str, Expense]:
        print("Reading expenses ...")

        if flags is not None:
            id_flag = flags.get("--id", None)
            if id_flag is not None:
                return self.get_single_expense(id_flag)

            category_flag = flags.get("--category", None)
            if category_flag is not None:
                return self.get_filtered_expenses(category_flag)

        return self.expenses

    def get_single_expense(self, id_flag: str):
        expense = self.expenses.get(int(id_flag))
        return {expense.pk: expense}

    def get_filtered_expenses(self, category_flag: str):
        return {
            expense_id: expense
            for (expense_id, expense) in self.expenses.items()
            if expense.category.name == category_flag
        }
