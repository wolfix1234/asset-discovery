#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.services import upsert_subdomain
from database.selectors import get_program_by_scope
from tools import crtsh
from utils import current_time


if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else False

    if not domain:
        print(f"Usage: watch_crtsh domain")
        sys.exit()

    program = get_program_by_scope(domain)

    if program:
        print(f"[{current_time()}] running Crtsh module for '{domain}'")
        subs = crtsh(domain)
        for sub in subs:
            upsert_subdomain(program.program_name, sub, "crtsh")
    else:
        print(f"[{current_time()}] scope for '{domain}' does not exist in watchtower")
