import sys
from workflow import Workflow3


def main(wf: Workflow3):
    args = sys.argv[1].split()
    quote = args[0]

    saved_quotes = wf.stored_data("saved_quotes")
    if not saved_quotes or quote not in saved_quotes:
        sys.stdout.write("Currency " + quote + " was not saved previously")
        return
    saved_quotes.remove(quote)
    wf.store_data("saved_quotes", saved_quotes)
    sys.stdout.write("Currency " + quote + " has been removed")


if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
