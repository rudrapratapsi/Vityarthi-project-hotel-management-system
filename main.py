"""Entry point: python main.py"""
import sys

from hotel import cli
from hotel.logger_setup import setup_logging
from hotel.storage import JsonStorage


def main():
    # Make sure the rupee symbol prints correctly on Windows terminals.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    setup_logging()
    try:
        cli.run(JsonStorage())
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram closed.")


if __name__ == "__main__":
    main()
