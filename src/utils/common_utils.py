import sys
from decimal import Decimal


def get_query() -> list[str]:
    return sys.argv[1].split()


def get_icon(currency: str) -> str:
    return "./src/assets/flags/" + currency + ".png"


def parse_amount(amount: str) -> Decimal:
    magnitude = {"k": 3, "K": 3, "m": 6, "M": 6, "b": 9, "B": 9}
    amount = amount.replace(",", "")

    if len(amount) == 0:
        return Decimal(1)

    if len(amount) == 1 and amount.isnumeric():
        return Decimal(amount)

    multiplier = 1
    if not amount[-1].isnumeric():
        if amount[-1] not in magnitude.keys():
            return Decimal(1)
        multiplier = 10 ** magnitude[amount[-1]]

    hasDot = False
    for i in range(len(amount) - 2, -1, -1):
        if amount[i] == ".":
            if hasDot:
                return Decimal(1)
            hasDot = True
            continue
        if not amount[i].isnumeric():
            return Decimal(1)

    return Decimal(amount) if multiplier == 1 else Decimal(amount[:-1]) * multiplier
