#!/usr/bin/env python3
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.selectors import get_http_services
from utils import send_discord_message, current_time
from tools import nuclei


if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else False

    if domain is False:
        print(f"Usage: watch_http domain")
        sys.exit()

    https_obj = get_http_services(scope=domain)

    if https_obj:
        print(f"[{current_time()}] running Nuclei module for all HTTP services")

        results = nuclei([http_obj.url for http_obj in https_obj])

        if results != "":
            send_discord_message(results)
