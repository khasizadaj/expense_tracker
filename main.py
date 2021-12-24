import sys
from typing import Dict, List

import config
from expense_tracker.database import Database
from expense_tracker.read import ReadExpensesFactory


def action_factory(action_type: str, expenses: Dict):
    return ReadExpensesFactory(expenses=expenses)


def get_action_flags(arguments: List[str]) -> Dict[str, str]:
    # TODO if there is no flag, use positions for provided arguments

    action_flags = {}
    for i, arg in enumerate(arguments):
        if arg.find("--") != -1:  # then argument is key
            action_flags[arg] = arguments[i + 1]

    return action_flags


def main(args: List[str]) -> None:
    if len(args) > 1:
        action_args = get_action_flags(args[1:])
    else:
        action_args = None

    database = Database(path=config.DATABASE_PATH)
    expenses = database.connect()

    factory = action_factory(args[0], expenses=expenses)
    result = factory.execute(action_args)
    print(result)


if __name__ == "__main__":
    args = sys.argv
    main(args[1:])
