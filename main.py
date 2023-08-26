import sys
from typing import Dict, List, Union

import loguru

import config
from expense_tracker.base import Expense, ExpensesFactory
from expense_tracker.create import CreateExpensesFactory
from expense_tracker.database import Database
from expense_tracker.read import ReadExpensesFactory

ACTIONS = ["create", "read"]  # "update", "delete", "summary", "analytics", "budget"


def action_factory(action_type: str, expenses: Dict) -> ExpensesFactory:
	"""Returns respective expense factory to handle the given action type."""

	if action_type not in ACTIONS:
		raise NotImplementedError("This action is not implemented.")

	if action_type == "create":
		factory = CreateExpensesFactory(expenses=expenses)
	elif action_type == "read":
		factory = ReadExpensesFactory(expenses=expenses)

	return factory


def get_action_flags(arguments: List[str]) -> Dict[str, str]:
	# TODO if there is no flag, use positions for provided arguments
	# TODO take into account whitespaces in some inputs

	action_flags = {}
	for i, arg in enumerate(arguments):
		if arg.find("--") != -1:  # then argument is key
			action_flags[arg] = arguments[i + 1]

	return action_flags


def print_result(is_pretty: str, result: Dict[str, Expense]):
	for pk, result_object in result.items():
		if is_pretty == "yes":
			print(pk, result_object)
		else:
			print(pk, repr(result_object))


@loguru.logger.catch()
def main(args: List[str]) -> None:
	if len(args) > 1:
		action_flags = get_action_flags(args[1:])
	else:
		action_flags = {}

	database = Database(path=config.DATABASE_PATH)
	expenses = database.connect()

	action_type = args[0]
	factory = action_factory(action_type, expenses=expenses)
	result = factory.execute(action_flags)

	if action_type in ["create", "update", "delete"]:
		database.save(list(result.values()))

	print_result(is_pretty=action_flags.get("--pretty", None), result=result)


if __name__ == "__main__":
	user_arguments = sys.argv
	main(user_arguments[1:])

	# user_arguments = ["main.py", "create"]
	# main(user_arguments[1:])
