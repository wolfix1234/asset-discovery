from database.models import Programs, Subdomains
from utils import get_domain_name, current_time, is_in_scope
from datetime import datetime

def upsert_subdomain(program_name, subdomain, provider):
    program = Programs.objects(program_name=program_name).first()
    subdomain = subdomain.lower()
    if not is_in_scope(subdomain, program.scopes, program.ooscopes):
        print(f"[{current_time()}] subdomain is not in scope: {subdomain}")
        return True

    existing = Subdomains.objects(program_name=program_name, subdomain=subdomain).first()

    if existing:
        if provider not in existing.providers:
            existing.providers.append(provider)
            existing.last_update = datetime.now()
            existing.save()
            print(f"[{current_time()}] Updated subdomain: {subdomain}")
    else:
        new_subdomain = Subdomains(
            program_name=program_name,
            subdomain=subdomain,
            scope=get_domain_name(subdomain),
            providers=[provider],
            created_date=datetime.now(),
            last_update=datetime.now()
        )
        new_subdomain.save()
        print(f"[{current_time()}] Inserted new subdomain: {subdomain}")
