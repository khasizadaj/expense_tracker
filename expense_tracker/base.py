import uuid
from dataclasses import dataclass
from decimal import Decimal
from typing import List

from expense_tracker.helper import shorten_pk


class Currency:
    currencies = {"1": "FT", "2": "EUR", "3": "USD", "4": "AZN"}

    def __init__(self, pk: str = "1"):
        self.pk = pk
        self.name = self.get_currency(pk)

    def get_currency(self, pk: str):
        return self.currencies[pk]

    def __repr__(self):
        return f'Currency(pk="{self.pk}")'

    def __str__(self):
        return f'Currency is "{self.name}".'

    @classmethod
    def stringify_currencies(cls):
        return "\n".join([pk + currency for (pk, currency) in cls.currencies.items()])

    @classmethod
    def get_currency_strings(cls):
        return cls.currencies.values()

    @classmethod
    def get_pk(cls, currency_input):
        for pk, currency in cls.currencies.items():
            if currency == currency_input:
                return pk
        return None


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
        return f'Category(name="{self.name}")'


@dataclass
class Expense:
    pk: str
    date: str
    amount: str
    name: str
    description: str
    currency: Currency = Currency()
    category: Category = Category()
    active: bool = True

    def __str__(self):
        return f'Expense of "{self.name}" that is incurred in {self.date} was amount of {self.currency.name} {self.amount}. It was for "{self.description}" and belongs to category of "{self.category.name}".'

    @property
    def short_pk(self):
        return shorten_pk(self.pk)

    @property
    def amount_decimal(self):
        decimal_amount = Decimal(self.amount).quantize(Decimal("1.0000"))
        return decimal_amount


class ExpensesFactory:
    def __init__(self, expenses):
        self._expenses = expenses

    @property
    def expenses(self):
        return self._expenses

    @property
    def expenses_as_list(self):
        self.expenses.values()
