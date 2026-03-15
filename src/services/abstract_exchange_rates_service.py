import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from utils import from_cache
from workflow.workflow3 import Workflow3


@dataclass(frozen=True)
class Currency:
    ccy_code: str
    ccy_name: str


@dataclass(frozen=True)
class ExchangeRates:
    base_ccy: str
    rates: dict[str, Decimal]


class AbstractExchangeRatesService(ABC):

    CACHE_CURRENCIES_KEY = "__CURRENCIES__"
    CACHE_EXCHANGE_RATES_BY_KEY = "__EXCHANGE_RATES_BY_{base_ccy}__"

    def __init__(self, workflow: Workflow3):
        self.wf = workflow

    def get_all_currencies(self) -> list[Currency]:
        return from_cache(
            self.CACHE_CURRENCIES_KEY,
            self._get_all_currencies_from_api,
            self.wf,
        )

    def get_exchange_rates_by_base_ccy(self, base_ccy: str) -> ExchangeRates:
        return from_cache(
            self.CACHE_EXCHANGE_RATES_BY_KEY.format(base_ccy=base_ccy),
            functools.partial(self._get_exchange_rates_by_base_ccy_from_api, base_ccy),
            self.wf,
        )

    @abstractmethod
    def _get_all_currencies_from_api(self) -> list[Currency]:
        pass

    @abstractmethod
    def _get_exchange_rates_by_base_ccy_from_api(self, base_ccy: str) -> ExchangeRates:
        pass
