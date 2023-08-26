import json
from typing import Dict, List

from expense_tracker.base import Category, Currency, Expense
from expense_tracker.helper import shorten_pk


class Database:
	def __init__(self, path):
		self.path = path

	def connect(self) -> Dict[str, Expense]:
		print("Connecting to database...")

		with open(self.path) as database_file:
			raw_expenses: List[Dict[str, str]] = json.load(database_file)

		expenses = {}
		for expense in raw_expenses:
			category = Category.get_or_create(name=expense["category"]["name"])
			currency = Currency(pk=expense["currency"]["pk"])

			short_pk = shorten_pk(expense["pk"])
			expenses[short_pk] = Expense(
				pk=expense["pk"],
				name=expense["name"],
				date=expense["date"],
				amount=expense["amount"],
				description=expense["description"],
				active=expense["active"],
				category=category,
				currency=currency,
			)

		return expenses

	def save(self, expenses: List[Expense]) -> None:
		with open(self.path, "w") as database_file:
			json.dump(expenses, database_file, default=vars, indent=2)
