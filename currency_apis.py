from workflow import Workflow3


def get_currencies_list():
    import requests

    wf = Workflow3()

    currencies_list = wf.stored_data("currencies_list")
    if currencies_list is not None:
        return currencies_list

    url = "https://api.exchangerate.host/latest"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    currencies_list = list(data["rates"].keys())

    wf.store_data("currencies_list", currencies_list)
    return currencies_list


def get_currency_rates(base: str):
    import requests

    url = "https://api.exchangerate.host/latest"

    res = requests.get(url, params={"base": base})
    res.raise_for_status()
    data = res.json()
    return data["rates"]
