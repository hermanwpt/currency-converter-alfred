from services.abstract_exchange_rates_service import (
    AbstractExchangeRatesService,
    Currency,
    ExchangeRates,
)
from workflow.workflow3 import Workflow3


class FreeExchangeRatesService(AbstractExchangeRatesService):

    API_BASE_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest"

    def __init__(self, workflow: Workflow3):
        super().__init__(workflow)

    def _get_all_currencies_from_api(self) -> list[Currency]:
        url = f"{self.API_BASE_URL}/v1/currencies.min.json"

        data = self._get(url)

        return [
            Currency(ccy_code=ccy_code.upper(), ccy_name=ccy_name)
            for ccy_code, ccy_name in data.items()
        ]

    def _get_exchange_rates_by_base_ccy_from_api(self, base_ccy: str) -> ExchangeRates:
        base_lower = base_ccy.lower()
        url = f"{self.API_BASE_URL}/v1/currencies/{base_lower}.json"

        data = self._get(url)

        rates = {
            quote_ccy.upper(): rate for quote_ccy, rate in data[base_lower].items()
        }
        return ExchangeRates(base_ccy=base_ccy.upper(), rates=rates)

    def _get(self, url: str):
        import requests

        res = requests.get(url)
        res.raise_for_status()
        return res.json()
