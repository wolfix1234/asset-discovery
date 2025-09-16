from database.models import Programs, Http
from utils import current_time, send_discord_message
from datetime import datetime


def upsert_http(subdomain, scope, ips, tech, title, status_code, headers, url, final_url, favicon):
    # {'subdomain': 'dl-api.voorivex.academy', 'scope': 'voorivex.academy', 'ips': ['185.166.104.4', '185.166.104.3'], 'tech': ['HSTS'], 'title': '', 'status_code': 403, 'headers': {'accept_ranges': 'bytes', 'cache_control': 'no-store', 'content_length': '15', 'content_type': 'text/html; charset=utf-8', 'date': 'Thu, 15 Aug 2024 12:45:17 GMT', 'server': 'Delivery', 'strict_transport_security': 'max-age=31536000', 'x_zrk_sn': '2001'}, 'url': 'https://dl-api.voorivex.academy:443', 'final_url': ''}

    program = Programs.objects(scopes=scope).first()
    # program.program_name

    # already existed http service
    existing = Http.objects(subdomain=subdomain).first()
    if existing:

        if existing.title != title:
            send_discord_message(f"```'{subdomain}' title has been changed from '{existing.title}' to '{title}'```")
            print(f"[{current_time()}] changes title for subdomain: {subdomain}")
            existing.title = title

        if existing.status_code != status_code:
            send_discord_message(f"```'{subdomain}' status code has been changed from '{existing.status_code}' to '{status_code}'```")
            print(f"[{current_time()}] changes status code for subdmoain: {subdomain}")
            existing.status_code = status_code

        
        if existing.favicon != favicon:
            send_discord_message(f"```'{subdomain}' favhash has been changed from '{existing.favicon}' to '{favicon}'```")
            print(f"[{current_time()}] changes favhash for subdomain: {subdomain}")
            existing.favicon = favicon

        existing.ips = ips
        existing.tech = tech
        existing.headers = headers
        existing.url = url
        existing.final_url = final_url
        existing.last_update = datetime.now()
        existing.save()

    else:
        new_http = Http(
            program_name = program.program_name,
            subdomain = subdomain,
            scope = scope,
            ips = ips,
            tech = tech,
            title = title,
            status_code = status_code,
            headers = headers,
            url = url,
            final_url = final_url,
            favicon = favicon,
            created_date = datetime.now(),
            last_update = datetime.now()
        )
        new_http.save()

        send_discord_message(f"```'{subdomain}' (fresh http) has been added to '{program.program_name}' program```")
        print(f"[{current_time()}] Inserted new http service: {subdomain}")

    return True