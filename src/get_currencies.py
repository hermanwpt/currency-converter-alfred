import sys

from services.abstract_exchange_rates_service import Currency
from services.free_exchange_rates_service import FreeExchangeRatesService
from utils import display_currency_not_found, get_ccy_icon, get_query
from workflow import MATCH_SUBSTRING, Workflow3


def main(wf: Workflow3):
    query = get_query()

    exchange_rates_service = FreeExchangeRatesService(workflow=wf)

    currencies = exchange_rates_service.get_all_currencies()

    filtered_currencies: list[Currency] = wf.filter(
        query[0],
        currencies,
        lambda c: f"{c.ccy_code} {c.ccy_name}",
        match_on=MATCH_SUBSTRING,
    )

    if not filtered_currencies:
        display_currency_not_found(query[0], wf)
        return

    for ccy in filtered_currencies:
        ccy_code, ccy_name = ccy.ccy_code, ccy.ccy_name
        wf.add_item(
            title=f"{ccy_code}: {ccy_name}",
            icon=get_ccy_icon(ccy_code),
            arg=ccy_code,
            valid=True,
        )

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3(libraries=["./lib"])
    sys.exit(wf.run(main))
