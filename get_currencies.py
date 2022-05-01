import sys
import json
from workflow import Workflow3, ICON_NOTE, MATCH_SUBSTRING
from currency_apis import get_currencies_set


def get_cur_code_with_name():
    cur_code_with_name = wf.stored_data("cur_code_with_name")
    if cur_code_with_name:
        return cur_code_with_name

    supported_cur = get_currencies_set()
    cur_code_to_name = json.load(open("./cur_code_to_name.json"))

    cur_code_with_name = set()
    for cur in supported_cur:
        if cur not in cur_code_to_name:
            continue
        cty = cur_code_to_name[cur]
        cur_code_with_name.add((cur, cty))

    wf.store_data("cur_code_with_name", cur_code_with_name)
    return cur_code_with_name


def main(wf: Workflow3):
    args = sys.argv[1].split()

    quote_new = None
    if len(args):
        quote_new = args[0]

    def key_for_quote(cur_code_with_name):
        return "{} {}".format(cur_code_with_name[0], cur_code_with_name[1])

    cur_code_with_name = get_cur_code_with_name()

    if quote_new:
        results = wf.filter(
            quote_new,
            cur_code_with_name,
            key_for_quote,
            match_on=MATCH_SUBSTRING,
        )

    if not results:
        wf.add_item("Currency " + quote_new + " Not Found", icon=ICON_NOTE)

    for r in results:
        wf.add_item(
            title=r[0] + ": " + r[1],
            icon="./flags/" + r[0] + ".png",
            arg=r[0],
            valid=True,
        )

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3(libraries=["./lib"])
    sys.exit(wf.run(main))
