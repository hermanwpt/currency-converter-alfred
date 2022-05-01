import sys
from workflow import Workflow3


def main(wf: Workflow3):
    query = sys.argv[1]
    args = query.split()
    quote = args[0]

    saved_quotes = wf.stored_data("saved_quotes")
    if saved_quotes is None:
        saved_quotes = []
    if quote not in saved_quotes:
        saved_quotes.append(quote)
        wf.store_data("saved_quotes", saved_quotes)
        sys.stdout.write("Currency " + quote + " has been added")
    else:
        sys.stdout.write("Currency " + quote + " is already added")


if __name__ == "__main__":
    wf = Workflow3(libraries=["./lib"])
    sys.exit(wf.run(main))
