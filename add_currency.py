import sys
from workflow import Workflow3


def main(wf: Workflow3):
    args = sys.argv[1].split()
    quote = args[0]

    saved_quotes = wf.stored_data("saved_quotes")
    if not saved_quotes:
        saved_quotes = []
    if quote in saved_quotes:
        sys.stdout.write(quote + " is already saved")
        return
    saved_quotes.append(quote)
    wf.store_data("saved_quotes", saved_quotes)
    sys.stdout.write(quote + " has been added")


if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
