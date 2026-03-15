import sys

from services.currency_service import CurrencyService
from utils import get_query
from workflow import Workflow3


def main(wf: Workflow3):
    query = get_query()
    ccy = query[0]

    ccy_service = CurrencyService(workflow=wf)

    tracked_ccy_codes = ccy_service.get_tracked_ccy_codes()

    if not tracked_ccy_codes or ccy not in tracked_ccy_codes:
        sys.stdout.write(f"{ccy} is not found")
        return

    ccy_service.remove_ccy_code(ccy)
    sys.stdout.write(f"{ccy} has been removed")


if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
