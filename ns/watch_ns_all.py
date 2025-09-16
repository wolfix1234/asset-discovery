#!/usr/bin/env python3
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.selectors import get_all_programs

from config import config
from utils import current_time, run_command_in_zsh


if __name__ == "__main__":
    programs = get_all_programs()

    for program in programs:
        for domain in program.scopes:
            print(f"[{current_time()}] name resolution for '{domain}' domain...")

            ns_path = config().get("WATCH_DIR") + "ns"
            run_command_in_zsh(f"python3 {ns_path}/watch_ns.py {domain}")
            # run_command_in_zsh(f"python3 {ns_path}/watch_ns_brute.py {domain}")
