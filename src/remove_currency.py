import sys
from workflow import Workflow3
from utils.common_utils import get_query


def main(wf: Workflow3):
    query = get_query()
    currency = query[0]

    saved_currencies = wf.stored_data("saved_currencies")
    if not saved_currencies or currency not in saved_currencies:
        sys.stdout.write(currency + " is not found")
        return
    saved_currencies.remove(currency)
    wf.store_data("saved_currencies", saved_currencies)
    sys.stdout.write(currency + " has been removed")


if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
