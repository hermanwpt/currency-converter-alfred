import re
from decimal import Decimal, InvalidOperation

from workflow.workflow3 import Workflow3


class CurrencyService:

    PERSIST_SAVED_CURRENCY_CODES_KEY = "__SAVED_CURRENCY_CODES__"

    _SUFFIX_MULTIPLIERS = {
        "k": Decimal(10) ** 3,
        "m": Decimal(10) ** 6,
        "b": Decimal(10) ** 9,
    }
    _AMOUNT_RE = re.compile(r"^\s*(?P<num>\d+(\.\d+)?)(?P<suffix>[kKmMbB])?\s*$")

    def __init__(self, workflow: Workflow3):
        self.wf = workflow

    def get_saved_currency_codes(self) -> set[str]:
        return self.wf.stored_data(self.PERSIST_SAVED_CURRENCY_CODES_KEY) or set()

    def add_currency_code(self, ccy_code: str) -> str:
        saved_currency_codes = self.get_saved_currency_codes()
        saved_currency_codes.add(ccy_code)
        self.wf.store_data(self.PERSIST_SAVED_CURRENCY_CODES_KEY, saved_currency_codes)
        return ccy_code

    def remove_currency_code(self, ccy_code: str) -> None:
        saved_currency_codes = self.get_saved_currency_codes()
        saved_currency_codes.remove(ccy_code)
        self.wf.store_data(self.PERSIST_SAVED_CURRENCY_CODES_KEY, saved_currency_codes)

    def compute_quote_ccy_amt(
        self, base_ccy: str, base_ccy_amt: Decimal, quote_ccy: str, rates: set
    ) -> Decimal:
        return base_ccy_amt / Decimal(rates[base_ccy]) * Decimal(rates[quote_ccy])

    def parse_amount(self, amount: str) -> Decimal:
        s = amount.replace(",", "")
        match = self._AMOUNT_RE.match(s)
        if not match:
            return Decimal(1)

        num_part = match.group("num")
        suffix = match.group("suffix")

        try:
            value = Decimal(num_part)
        except InvalidOperation:
            return Decimal(1)

        if suffix:
            value *= self._SUFFIX_MULTIPLIERS[suffix.lower()]

        return value
