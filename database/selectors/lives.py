from database.models import Subdomains, LiveSubdomains

from datetime import datetime, timedelta


def get_single_live(subdomain):
    return LiveSubdomains.objects(subdomain=subdomain).first()


def get_lives(
    program=None,
    scope=None,
    provider=None,
    tag=None,
    fresh=False,
    count=False,
    limit=None,
    page=None,
):
    filters = {}
    if program:
        filters["program_name"] = program
    if scope:
        filters["scope"] = scope
    if fresh:
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        filters["created_date__gte"] = twenty_four_hours_ago
    if provider:
        twelve_hours_ago = datetime.now() - timedelta(hours=12)
        subdomains = Subdomains.objects(providers=[provider])
        sub_urls = [sub.subdomain for sub in subdomains]
        filters["subdomain__in"] = sub_urls
        filters["last_update__gte"] = twelve_hours_ago
    if tag:
        filters["tag"] = tag

    subdomains = LiveSubdomains.objects(**filters)
    if count:
        return subdomains.count()

    if limit is not None and page is not None:
        offset = (page - 1) * limit
        subdomains = subdomains.skip(offset).limit(limit)

    return subdomains
