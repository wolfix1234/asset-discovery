#!/usr/bin/env python3
import tempfile
import os

from utils import run_command_in_zsh


class Colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"


def dnsx(subdomains_array, domain):
    # Create a temporary file to store the list of subdomains
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_file:
        for sub in subdomains_array:
            temp_file.write(f"{sub}\n")

    subdomains_file = temp_file.name

    # Define the command to run dnsx with specified parameters
    command = (
        f"dnsx -l {subdomains_file} -silent -wd {domain} -resp -json "
        f"-rl 30 -t 10 -r 8.8.4.4,129.250.35.251,208.67.222.222"
    )

    print(f"{Colors.GRAY}Executing command: {command}{Colors.RESET}")

    # Execute the command and capture the results
    results = run_command_in_zsh(command)
    os.remove(subdomains_file)
    # Process the results and upsert live subdomains into the database

    return results
