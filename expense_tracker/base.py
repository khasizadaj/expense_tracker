from dataclasses import dataclass

CURRENCIES = {"1": "FT", "2": "EUR", "3": "USD", "4": "AZN"}


@dataclass
class Currency:
    id: str
    name: str

    def __init__(self, id: str = "1"):
        self.id = id
        self.name = self.get_currency(id)

    def get_currency(self, id: str):
        return CURRENCIES[id]


@dataclass
class Category:
    id: int = 1
    name: str = "General"


@dataclass
class Expense:
    id: str
    date: str
    amount: float
    name: str
    description: str
    active: bool = True
    currency: Currency = Currency()
    category: Category = Category()

    def __str__(self):
        return f'Expense of "{self.name}" that is incurred in {self.date} was amount of {self.currency.name} {self.amount}. It was for "{self.description}" and belongs to category of "{self.category.name}".'


class ExpensesFactory:
    def __init__(self, expenses):
        self._expenses = expenses

    @property
    def expenses(self):
        return self._expenses
