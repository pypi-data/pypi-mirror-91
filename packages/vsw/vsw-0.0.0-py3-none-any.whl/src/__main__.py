#!/usr/bin/env python3
import sys
from typing import Any

from src import cli


def main() -> Any:
    print('Welcome to vsw command line!')
    cli.dispatch(sys.argv[1:])

if __name__ == "__main__":
    sys.exit(main())
