import os
import sys


def main():
    from pylogview import logview

    logview()


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    main()
