from decimal import Decimal


def get_supported_currencies() -> list:
    import requests

    url = "https://api.exchangerate.host/latest"

    res = requests.get(url)
    res.raise_for_status()
    data = res.json()

    return list(data["rates"].keys())


def get_currency_rates(base: str):
    import requests

    url = "https://api.exchangerate.host/latest"

    res = requests.get(url, params={"base": base})
    res.raise_for_status()
    data = res.json()

    return data["rates"]


def get_quote_amount(base: str, base_amount: Decimal, quote: str, rates: set):
    return base_amount / Decimal(rates[base]) * Decimal(rates[quote])
