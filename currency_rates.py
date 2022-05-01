import sys
import functools
from workflow import Workflow3, ICON_NOTE, MATCH_STARTSWITH
from currency_apis import get_currencies_set, get_currency_rates, get_quote_val

# args[0]: base
# args[1]: base_val (optional)
# args[2]: quote (optional)
def main(wf: Workflow3):
    args = sys.argv[1].split()

    if not len(args):
        return

    saved_quotes = wf.stored_data("saved_quotes")
    if not saved_quotes:
        wf.add_item(title="Please Add A Currency", icon=ICON_NOTE)
        wf.send_feedback()
        return

    base = args[0].upper()
    base_val = 1.0
    if len(args) > 1:
        base_val = float(args[1])
    supported_currencies = get_currencies_set()

    # Results filter logic
    allResults = []
    savedResults = wf.filter(base, saved_quotes, match_on=MATCH_STARTSWITH)
    # base not in saved_quotes --> find in all currencies
    if not savedResults:
        allResults = wf.filter(base, supported_currencies, match_on=MATCH_STARTSWITH)
        # base invalid --> error msg
        if not allResults:
            wf.add_item(title="Currency " + base + " Not Found", icon=ICON_NOTE)
            wf.send_feedback()
            return
        base = allResults[0]
    else:
        base = savedResults[0]

    rates = wf.cached_data(
        "rates", functools.partial(get_currency_rates, "USD"), max_age=900
    )

    # Case 1: base --> saved_quotes
    if len(args) < 3:
        for quote in allResults:
            val = get_quote_val(base, base_val, quote, rates)
            wf.add_item(
                title=val,
                subtitle=quote,
                icon="./flags/" + quote + ".png",
                autocomplete=quote,
            )
        if savedResults:
            val = get_quote_val(base, base_val, base, rates)
            wf.add_item(
                title=val,
                subtitle=base,
                icon="./flags/" + base + ".png",
                autocomplete=base,
                arg=(base, val),
                valid=True,
            )
        for quote in saved_quotes:
            if base == quote:
                continue
            val = get_quote_val(base, base_val, quote, rates)
            wf.add_item(
                title=val,
                subtitle=quote,
                icon="./flags/" + quote + ".png",
                autocomplete=quote,
                arg=(quote, val),
                valid=True,
            )

    # Case 2: base --> quote
    else:
        quote = args[2].upper()
        allQuotes = wf.filter(quote, supported_currencies, match_on=MATCH_STARTSWITH)
        for quote in allQuotes:
            val = base_val * rates[quote]
            wf.add_item(
                title=val,
                subtitle=quote,
                icon="./flags/" + quote + ".png",
                autocomplete=quote,
                arg=(quote, val),
                valid=True,
            )

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3(libraries=["./lib"])
    sys.exit(wf.run(main))
