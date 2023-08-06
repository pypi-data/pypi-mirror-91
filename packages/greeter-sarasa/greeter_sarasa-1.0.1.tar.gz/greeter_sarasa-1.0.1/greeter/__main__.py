import argparse
import os
import sys

from greeter.greeter import Greeter


CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yml")


def main():
    parser = argparse.ArgumentParser(description="Un saludador profesional.")
    parser.add_argument("name", help="Tu nombre")
    user_name = parser.parse_args().name
    try:
        Greeter(user_name, config_file=CONFIG_FILE).greet()
    except Exception:
        print("Whoops, something went wrong", file=sys.stderr)
