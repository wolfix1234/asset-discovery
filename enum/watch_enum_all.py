#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.selectors import get_all_programs

from utils import current_time, run_command_in_zsh
from config import config


if __name__ == "__main__":
    programs = get_all_programs()

    for program in programs:
        print(f"[{current_time()}] let's go for '{program.program_name}' program...")
        scopes = program.scopes

        for scope in scopes:
            print(f"[{current_time()}] enumerating subdomains for '{scope}' domain...")
            enum_path = config().get("WATCH_DIR") + "enum"

            for provider in program.config["providers"]:
                run_command_in_zsh(f"python3 {enum_path}/watch_{provider}.py {scope}")
