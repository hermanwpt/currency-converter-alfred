import sys

from services.currency_service import CurrencyService
from utils import get_query
from workflow import Workflow3


def main(wf: Workflow3):
    query = get_query()
    ccy = query[0]

    ccy_service = CurrencyService(workflow=wf)

    tracked_ccy_codes = ccy_service.get_tracked_ccy_codes()

    if tracked_ccy_codes and ccy in tracked_ccy_codes:
        sys.stdout.write(f"{ccy} is already saved")
        return

    ccy_service.add_ccy_code(ccy)
    sys.stdout.write(f"{ccy} has been added")


if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
