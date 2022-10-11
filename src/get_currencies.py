import sys
import json
from workflow import Workflow3, ICON_NOTE, MATCH_SUBSTRING
from currency_apis import get_supported_currencies
from utils.common_utils import get_query, get_icon


def get_currencies_code_name() -> set[tuple]:
    currency_code_name_map = json.load(open("./src/assets/currency_code_name_map.json"))
    return set(
        (cur, currency_code_name_map[cur])
        for cur in get_supported_currencies()
        if cur in currency_code_name_map
    )


def main(wf: Workflow3):
    query = get_query()
    new_currency = query[0]

    currencies_code_name = wf.cached_data(
        "currencies_code_name", get_currencies_code_name, 60 * 60 * 24
    )

    results = wf.filter(
        new_currency,
        currencies_code_name,
        lambda code_name: "{} {}".format(code_name[0], code_name[1]),
        match_on=MATCH_SUBSTRING,
    )

    if not results:
        wf.add_item("Currency Not Found", icon=ICON_NOTE)

    for res in results:
        wf.add_item(
            title=res[0] + ": " + res[1],
            icon=get_icon(res[0]),
            arg=res[0],
            valid=True,
        )

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3(libraries=["./lib"])
    sys.exit(wf.run(main))
