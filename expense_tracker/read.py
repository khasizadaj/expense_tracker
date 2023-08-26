from typing import Dict, Optional
from expense_tracker.base import Expense, ExpensesFactory
from expense_tracker.helper import shorten_pk


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
		expense = self.expenses.get(id_flag)
		return {shorten_pk(expense.pk): expense}

	def get_filtered_expenses(self, category_flag: str):
		return {
			shorten_pk(pk): expense
			for (pk, expense) in self.expenses.items()
			if expense.category.name == category_flag
		}
