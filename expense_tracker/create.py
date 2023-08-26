import uuid
from datetime import datetime
from typing import Dict, Optional

from expense_tracker.base import Category, Currency, Expense, ExpensesFactory


class CreateExpensesFactory(ExpensesFactory):

	input_messages = {
		"amount": "What is the amount of expense?:\n",
		"name": "What is the name of the expense?:\n",
		"description": "Do you wanna add a description? (Press enter if you want to keep it empty)\n",
		"category": "What is the category of the expense?:\n",
		"currency": f"What is the currency of the expense? (Select number or type cyrrency.): \n{Currency.stringify_currencies()}\n",
		"one-line-inputs": "Please provide all the inputs in the this order and use semicolons to separate them: amount, name, description, category, currency. \n\nNote: If you want to use default value, keep it empty.\n",
	}

	user_input_flags = [
		"--amount",
		"--name",
		"--description",
		"--category",
		"--currency",
	]

	def execute(self, flags: Dict[str, str]) -> Dict[int, Expense]:
		expense_details = self.get_expense_inputs(flags)
		expense = self.generate_expense(expense_details)
		return self.add_to_database(expense)

	def add_to_database(self, expense):
		self.expenses[expense.short_pk] = expense
		return self.expenses

	def process_inputs_with_flag(self, flags: Dict[str, str]) -> Dict[str, str]:
		amount = self.convert_to_decimal_string(flags.get("--amount"))
		name = flags.get("--name")
		description = flags.get("--description")
		category = flags.get("--category")
		currency_pk = flags.get("--currency")

		expense_pk = uuid.uuid4().hex
		date = datetime.today().strftime("%d.%m.%Y")

		return self.get_expense_inputs_dict(
			amount=amount,
			name=name,
			description=description,
			category=category,
			currency_pk=currency_pk,
			expense_pk=expense_pk,
			date=date,
		)

	def process_inputs_one_line(self) -> Dict[str, str]:
		inputs = input(self.input_messages["one-line-inputs"]).split(";")

		amount = self.convert_to_decimal_string(inputs[0])
		name = inputs[1]
		description = inputs[2]
		category = inputs[3]
		currency_pk = inputs[4]

		expense_pk = uuid.uuid4().hex
		date = datetime.today().strftime("%d.%m.%Y")

		return self.get_expense_inputs_dict(
			amount=amount,
			name=name,
			description=description,
			category=category,
			currency_pk=currency_pk,
			expense_pk=expense_pk,
			date=date,
		)

	def process_inputs_ask_each_input(self) -> Dict[str, str]:
		currency_input = input(self.input_messages["currency"]).upper()
		if currency_input.isnumeric():
			currency_pk = currency_input
		elif currency_input.isalpha():
			if currency_input in Currency.get_currency_strings():
				pk = Currency.get_pk(currency_input)
				if pk is not None:
					currency_pk = pk

		amount = self.convert_to_decimal_string(input(self.input_messages["amount"]))
		name = input(self.input_messages["name"])
		description = input(self.input_messages["description"])
		category = input(self.input_messages["category"])

		# TODO ask again if provided input is incorrect

		expense_pk = uuid.uuid4().hex
		date = datetime.today().strftime("%d.%m.%Y")

		return self.get_expense_inputs_dict(
			amount=amount,
			name=name,
			description=description,
			category=category,
			currency_pk=currency_pk,
			expense_pk=expense_pk,
			date=date,
		)

	def get_expense_inputs(self, flags: Dict[str, str]) -> Dict[str, str]:
		# TODO check if optional or required

		# TODO flags - user can specify if he/she wants to add inputs one-by-one
		# or in one line with order of inputs;
		# flag name: --one-line-inputs

		flags = flags.copy()
		one_line_inputs = flags.get("--one-line-inputs", False)
		inputs_provided_with_flag = self.check_inputs_provided_with_flag(flags)

		if inputs_provided_with_flag:
			expense_dict = self.process_inputs_with_flag(flags)

		elif one_line_inputs:
			expense_dict = self.process_inputs_one_line()

		else:
			expense_dict = self.process_inputs_ask_each_input()

		return expense_dict

	def check_inputs_provided_with_flag(self, flags: Dict[str, str]):
		keys = list(flags.keys())
		keys.sort()
		self.user_input_flags.sort()

		return keys == self.user_input_flags

	def generate_expense(self, flags: Dict[str, str]) -> Expense:
		category = Category.get_or_create(name=flags.get("--category"))
		currency = Currency(pk=flags.get("--currency_pk"))

		expense = Expense(
			pk=flags.get("--pk"),
			name=flags.get("--name"),
			date=flags.get("--date"),
			amount=flags.get("--amount"),
			description=flags.get("--description"),
			category=category,
			currency=currency,
		)

		return expense

	def convert_to_decimal_string(self, amount_string: str):
		"""
		If comma is used as decimal seperator, it replaces it with point seperator.
		"""

		return amount_string.replace(",", ".")

	@staticmethod
	def get_expense_inputs_dict(
		*,
		amount: str,
		name: str,
		description: str,
		category: str,
		currency_pk: str,
		expense_pk: str,
		date: str,
	):
		expense_inputs = {
			"--pk": expense_pk,
			"--date": date,
			"--amount": amount,
			"--name": name,
			"--description": description,
			"--category": category,
			"--currency_pk": currency_pk,
		}

		return expense_inputs
