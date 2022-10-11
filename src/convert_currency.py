import sys
import functools
from decimal import Decimal
from re import sub
from workflow import Workflow3, ICON_NOTE, MATCH_STARTSWITH
from currency_apis import get_supported_currencies, get_currency_rates, get_quote_amount
from utils.common_utils import get_query, get_icon, parse_amount


def wf_add_quote(
    wf: Workflow3, base: str, base_amount: Decimal, quote: str, rates: dict
):
    quote_amount_trimmed = "{:,.2f}".format(
        get_quote_amount(base, base_amount, quote, rates)
    )
    wf.add_item(
        title=quote_amount_trimmed,
        subtitle=quote,
        icon=get_icon(quote),
        autocomplete=quote,
        arg=(quote, quote_amount_trimmed),
        valid=True,
    )


def main(wf: Workflow3):
    query = get_query()
    if len(query) == 0:
        return

    base_query = query[0].upper()
    saved_currencies = wf.stored_data("saved_currencies") or []
    if not saved_currencies:
        saved_currencies = ["USD"]
        wf.store_data("saved_currencies", saved_currencies)
    supported_currencies = wf.cached_data(
        "supported_currencies", get_supported_currencies, 60 * 60 * 24
    )
    rates = wf.cached_data(
        "rates", functools.partial(get_currency_rates, "USD"), 60 * 15
    )

    saved_results = wf.filter(base_query, saved_currencies, match_on=MATCH_STARTSWITH)
    results = []
    base = "USD"
    if saved_results:
        base = saved_results[0]
    else:
        results = wf.filter(base_query, supported_currencies, match_on=MATCH_STARTSWITH)
        if not results:
            wf.add_item(title="Currency " + base_query + " Not Found", icon=ICON_NOTE)
            wf.send_feedback()
            return
        base = results[0]
    base_amount = parse_amount(query[1]) if len(query) >= 2 else Decimal(1)

    if len(query) <= 2:
        for quote in results:
            wf_add_quote(wf, base, base_amount, quote, rates)
        if saved_results:
            wf_add_quote(wf, base, base_amount, base, rates)
        for quote in saved_currencies:
            if base == quote:
                continue
            wf_add_quote(wf, base, base_amount, quote, rates)
        wf.send_feedback()
        return

    quote_query = query[2].upper()
    quote_results = wf.filter(
        quote_query, supported_currencies, match_on=MATCH_STARTSWITH
    )
    if not quote_results:
        wf.add_item(title="Currency " + quote_query + " Not Found", icon=ICON_NOTE)
    for quote in quote_results:
        wf_add_quote(wf, base, base_amount, quote, rates)

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3(libraries=["./lib"])
    sys.exit(wf.run(main))
