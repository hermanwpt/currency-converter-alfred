from re import sub
import sys
import functools
from workflow import Workflow3
from workflow.workflow import ICON_NOTE
from currency_apis import get_currencies_list, get_currency_rates

# args[0]: base
# args[1]: base_val (optional)
# args[2]: quote (optional)
def main(wf: Workflow3):
    query = sys.argv[1]
    args = query.split()

    # return if no args
    if len(args) < 1:
        return

    # return if no saved currency
    saved_quotes = wf.stored_data("saved_quotes")
    if saved_quotes is None:
        wf.add_item(title="No Currency Is Saved", icon=ICON_NOTE)
        wf.send_feedback()
        return

    base_val = 1.0
    if len(args) > 1:
        base_val = float(args[1])
    base = args[0].upper()
    supported_currencies = get_currencies_list()

    # Filter logic
    savedResults = wf.filter(base, saved_quotes)
    # base not in saved_quotes
    if not savedResults:
        allResults = wf.filter(base, supported_currencies)
        # base is invalid
        if not allResults:
            wf.add_item(title="Currency " + base + " Not Found", icon=ICON_NOTE)
            wf.send_feedback()
            return
        base = allResults[0]
    else:
        base = savedResults[0]

    # Get exchange rates with base
    rates = wf.cached_data(
        "rates:" + base, functools.partial(get_currency_rates, base), max_age=3600
    )

    # Case 1: base --> quote
    if len(args) > 2:
        quote = args[2].upper()
        if quote in rates.keys():
            wf.add_item(
                title=base_val * rates[quote],
                subtitle=quote,
                icon="./flags/" + quote + ".png",
            )
    # Case 2: base --> saved_quotes
    else:
        if len(savedResults) == 0 and base not in supported_currencies:
            for quote in allResults:
                wf.add_item(
                    title=base_val * rates[quote],
                    subtitle=quote,
                    icon="./flags/" + quote + ".png",
                )
        else:
            wf.add_item(
                title=base_val * rates[base],
                subtitle=base,
                icon="./flags/" + base + ".png",
            )
            for quote in saved_quotes:
                if base == quote:
                    continue
                wf.add_item(
                    title=base_val * rates[quote],
                    subtitle=quote,
                    icon="./flags/" + quote + ".png",
                )

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3(libraries=["./lib"])
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))
