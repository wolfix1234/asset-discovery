#!/usr/bin/env python3
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
            print(f"[{current_time()}] running HTTP service discovery for '{domain}' domain...")

            http_path = config().get("WATCH_DIR") + "http"
            run_command_in_zsh(f"python3 {http_path}/watch_http.py {domain}")
