from workflow import Workflow3


def get_currencies_set():
    import requests

    wf = Workflow3()

    currencies_set = wf.stored_data("currencies_set")
    if currencies_set is not None:
        return currencies_set

    url = "https://api.exchangerate.host/latest"

    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    currencies_set = set(data["rates"].keys())
    wf.store_data("currencies_set", currencies_set)

    return currencies_set


def get_currency_rates(base: str):
    import requests

    url = "https://api.exchangerate.host/latest"

    res = requests.get(url, params={"base": base})
    res.raise_for_status()
    data = res.json()

    return data["rates"]


def get_quote_val(base: str, base_val: float, quote: str, rates: set):
    return base_val / rates[base] * rates[quote]
