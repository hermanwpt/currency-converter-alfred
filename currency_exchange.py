import sys
import json
import functools

from workflow import Workflow3

query = sys.argv[1]
client_cur = "HKD"
client_quotes = ["HKD", "USD", "GBP", "JPY"]


# def get_client_saved_quotes():


def get_currency_rates(base):
    import requests

    url = "https://api.exchangerate.host/latest"

    response = requests.get(url, params={"base": base})
    response.raise_for_status()
    data = response.json()
    return data["rates"]


# base --> quote
def main(wf):
    args = query.split()
    num_of_args = len(args)

    base_val = 1.0
    if num_of_args == 0:
        base = client_cur
    else:
        if num_of_args >= 2:
            base_val = float(args[1])
        base = args[0].upper()
    rates = wf.cached_data(
        "rates:" + base, functools.partial(get_currency_rates, base), max_age=3600
    )

    if num_of_args >= 3:
        quote = args[2].upper()
        if quote in rates.keys():
            wf.add_item(quote, base_val * rates[quote])
    else:
        for quote in client_quotes:
            if quote in rates.keys():
                wf.add_item(quote, base_val * rates[quote])

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3(libraries=["./lib"])
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))

# TODO: icon
