from typing import List
from dataclasses import dataclass
import uuid

CURRENCIES = {"1": "FT", "2": "EUR", "3": "USD", "4": "AZN"}


class Currency:
    def __init__(self, pk: str = "1"):
        self.pk = pk
        self.name = self.get_currency(pk)

    def get_currency(self, pk: str):
        return CURRENCIES[pk]

    def __repr__(self):
        return f'Currency(pk="{self.pk}")'

    def __str__(self):
        return f'Currency is "{self.name}".)'


class Category:
    instances = {}

    def __init__(self, name: str = "General"):
        self.pk = uuid.uuid4().hex
        self.name = name

    @classmethod
    def get_or_create(cls, name: str):
        category = [obj for (_, obj) in cls.instances.items() if obj.name == name]

        if len(category) > 1:
            return category[0]

        new_category = cls(name=name)
        cls.instances[new_category.pk] = new_category
        return new_category

    def __repr__(self):
        return f'Category(name="{self.name}")'`


@dataclass
class Expense:
    pk: str
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
