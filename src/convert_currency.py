import sys
from decimal import Decimal

from services.currency_service import CurrencyService
from services.free_exchange_rates_service import FreeExchangeRatesService
from utils import display_currency_not_found, get_ccy_icon, get_query
from workflow import MATCH_STARTSWITH, Workflow3

_INTERNAL_BASE_CCY = "USD"


def _get_tracked_ccy_codes_with_default(ccy_service: CurrencyService):
    tracked = ccy_service.get_tracked_ccy_codes()
    if not tracked:
        ccy_service.add_ccy_code(_INTERNAL_BASE_CCY)
        tracked = ccy_service.get_tracked_ccy_codes()
    return tracked


def _compute_base_ccy_and_quote_ccy_list(
    wf: Workflow3,
    query_token: str,
    tracked_codes: set[str],
    all_codes: set[str],
) -> tuple[str, list[str]]:
    token_upper = query_token.upper()

    filtered_tracked = wf.filter(token_upper, tracked_codes, match_on=MATCH_STARTSWITH)
    if filtered_tracked:
        matched = filtered_tracked[0]
        reordered_tracked = [matched] + [c for c in tracked_codes if c != matched]
        return matched, reordered_tracked

    filtered_all = wf.filter(token_upper, all_codes, match_on=MATCH_STARTSWITH)
    if filtered_all:
        matched = filtered_all[0]
        all_plus_tracked_codes = filtered_all + list(tracked_codes)
        reordered_all = [matched] + [c for c in all_plus_tracked_codes if c != matched]
        return matched, reordered_all

    return None, []


def _display_quote_ccy_amounts(
    wf: Workflow3,
    ccy_service: CurrencyService,
    base_ccy: str,
    base_ccy_amt: Decimal,
    rates,
    quote_ccy_list: list[str],
):
    for quote_ccy in quote_ccy_list:
        quote_ccy_amt = "{:,.2f}".format(
            ccy_service.compute_quote_ccy_amt(base_ccy, base_ccy_amt, quote_ccy, rates)
        )
        wf.add_item(
            title=quote_ccy_amt,
            subtitle=quote_ccy,
            icon=get_ccy_icon(quote_ccy),
            autocomplete=quote_ccy,
            arg=(quote_ccy, quote_ccy_amt),
            valid=True,
        )


def main(wf: Workflow3):
    query = get_query()
    if not query:
        return

    ccy_service = CurrencyService(workflow=wf)
    exchange_rates_service = FreeExchangeRatesService(workflow=wf)

    tracked_codes = _get_tracked_ccy_codes_with_default(ccy_service)
    all_codes = {ccy.ccy_code for ccy in exchange_rates_service.get_all_currencies()}
    rates = exchange_rates_service.get_exchange_rates_by_base_ccy(
        _INTERNAL_BASE_CCY
    ).rates

    base_ccy, quote_ccy_list = _compute_base_ccy_and_quote_ccy_list(
        wf, query[0], tracked_codes, all_codes
    )
    if not base_ccy:
        display_currency_not_found(query[0].upper(), wf)
        return

    base_ccy_amt = ccy_service.parse_amount(query[1]) if len(query) >= 2 else Decimal(1)

    if len(query) <= 2:
        _display_quote_ccy_amounts(
            wf, ccy_service, base_ccy, base_ccy_amt, rates, quote_ccy_list
        )
    else:
        quote_ccy_matches = wf.filter(
            query[2].upper(), all_codes, match_on=MATCH_STARTSWITH
        )
        if not quote_ccy_matches:
            display_currency_not_found(query[2].upper(), wf)
            return
        _display_quote_ccy_amounts(
            wf, ccy_service, base_ccy, base_ccy_amt, rates, quote_ccy_matches
        )

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3(libraries=["./lib"])
    sys.exit(wf.run(main))
