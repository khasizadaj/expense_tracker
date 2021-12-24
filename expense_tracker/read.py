from typing import Dict, Optional
from expense_tracker.base import ExpensesFactory


class ReadExpensesFactory(ExpensesFactory):
    def execute(self, flags: Optional[Dict[str, str]]) -> Dict[str, str]:
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
        return self.expenses.get(id_flag)

    def get_filtered_expenses(self, category_flag: str):
        return {
            expense_id: expense
            for (expense_id, expense) in self.expenses.items()
            if expense.category == category_flag
        }
