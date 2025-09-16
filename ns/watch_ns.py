#!/usr/bin/env python3
import sys
import json
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.services import upsert_lives
from database.selectors import get_subdomains

from tools import dnsx

from utils import current_time, get_ip_tag


if __name__ == "__main__":
    # Get the domain from command-line arguments
    domain = sys.argv[1] if len(sys.argv) > 1 else False

    if not domain:
        print("Usage: watch_ns <domain>")
        sys.exit()

    # Retrieve subdomains associated with the given domain from the database
    obj_subs = get_subdomains(scope=domain)

    if obj_subs:
        print(f"[{current_time()}] Running Dnsx module for '{domain}'")

        # Call the dnsx function with the list of subdomains and domain name
        results = dnsx([obj_sub.subdomain for obj_sub in obj_subs], domain)

        for result in results:
            obj = json.loads(result)
            tag = get_ip_tag(obj.get("a"))
            upsert_lives(
                domain=domain,
                subdomain=obj.get("host"),
                ips=obj.get("a"),
                tag=tag,
            )
    else:
        print(f"[{current_time()}] Domain '{domain}' does not exist in watchtower")
