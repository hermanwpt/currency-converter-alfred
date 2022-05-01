import sys
from workflow import Workflow3
from workflow.workflow import ICON_NOTE
from currency_apis import get_currencies_set


def main(wf: Workflow3):
    args = sys.argv[1].split()

    quote_new = None
    if len(args):
        quote_new = args[0]

    supported_currencies = get_currencies_set()

    if quote_new:
        supported_currencies = wf.filter(quote_new, supported_currencies)

    if not supported_currencies:
        wf.add_item("Currency " + quote_new + " Not Found", icon=ICON_NOTE)

    for currency in supported_currencies:
        wf.add_item(
            title=currency,
            icon="./flags/" + currency + ".png",
            arg=currency,
            valid=True,
        )

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3(libraries=["./lib"])
    sys.exit(wf.run(main))
