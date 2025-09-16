#!/usr/bin/env python3
import sys, re, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.services import upsert_subdomain
from database.selectors import get_program_by_scope

from tools import subfinder

from utils import current_time


if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else False

    if not domain:
        print(f"Usage: watch_subfinder domain")
        sys.exit()

    program = get_program_by_scope(domain)

    if program:
        print(f"[{current_time()}] running Subfinder module for '{domain}'")
        subs = subfinder(domain)
        for sub in subs:
            if re.search(r"\.\s*" + re.escape(domain), sub, re.IGNORECASE):
                upsert_subdomain(program.program_name, sub, "subfinder")
    else:
        print(f"[{current_time()}] scope for '{domain}' does not exist in watchtower")
