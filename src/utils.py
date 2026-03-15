import sys
from typing import Callable, TypeVar

from workflow.workflow import ICON_NOTE
from workflow.workflow3 import Workflow3

_DEFAULT_CACHE_TTL_SECONDS = 60 * 15
R = TypeVar("R")


def from_cache(
    key: str,
    func: Callable[..., R],
    wf: Workflow3,
    cache_ttl_seconds: int = _DEFAULT_CACHE_TTL_SECONDS,
) -> R:
    return wf.cached_data(
        key,
        func,
        cache_ttl_seconds,
    )


def display_currency_not_found(ccy_code: str, wf: Workflow3) -> None:
    wf.add_item(title=f"Currency {ccy_code} Not Found", icon=ICON_NOTE)
    wf.send_feedback()


def get_query() -> list[str]:
    return sys.argv[1].split()


def get_ccy_icon(currency: str) -> str:
    return f"./src/assets/flags/{currency}.png"
