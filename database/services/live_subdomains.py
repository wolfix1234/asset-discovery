from database.models import Programs, LiveSubdomains
from utils import current_time, send_discord_message
from datetime import datetime


def upsert_lives(domain, subdomain, ips, tag):
    subdomain = subdomain.lower()
    program = Programs.objects(scopes=domain).first()
    existing = LiveSubdomains.objects(subdomain=subdomain).first()

    if existing:
        existing.ips.sort()
        ips.sort()
        if ips != existing.ips:
            existing.ips = ips
            print(f"[{current_time()}] Updated live subdomain: {subdomain}")
        existing.last_update = datetime.now()
        existing.save()
    else:
        new_live_subdomain = LiveSubdomains(
            program_name=program.program_name,
            subdomain=subdomain,
            scope=domain,
            ips=ips,
            tag=tag,
            created_date=datetime.now(),
            last_update=datetime.now(),
        )
        new_live_subdomain.save()
        send_discord_message(f"```'{subdomain}' (fresh live) has been added to '{program.program_name}' program```")
        print(f"[{current_time()}] Inserted new live subdomain: {subdomain}")

    return True
