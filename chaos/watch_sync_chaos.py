#!/usr/bin/env python3
import tempfile
import shutil
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import run_command_in_zsh
from config import config


class Colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"


CHAOS_FOLDER = config().get("WATCH_DIR") + "chaos/"


def download_and_unzip():
    # Create a temporary directory for downloads
    with tempfile.TemporaryDirectory() as temp_dir:
        # Command to download and unzip files
        curl_command = (
            f"cd {temp_dir} && "
            "curl -s https://chaos-data.projectdiscovery.io/index.json | "
            'jq -r ".[].URL" | '
            "while read url; do wget -q $url && unzip -q $(echo $url | rev | cut -d / -f 1 | rev); done && rm -rf *.zip"
        )

        # Execute the command
        print(f"{Colors.GRAY}Executing command: {curl_command}{Colors.RESET}")
        run_command_in_zsh(curl_command)

        # Move the files from temp_dir to CHAOS_FOLDER
        for filename in os.listdir(temp_dir):
            shutil.move(os.path.join(temp_dir, filename), CHAOS_FOLDER)

        print("Files downloaded and unzipped successfully.")


if __name__ == "__main__":
    download_and_unzip()
