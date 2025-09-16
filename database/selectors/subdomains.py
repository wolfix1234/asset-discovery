from database.models import Subdomains
from datetime import datetime, timedelta


def get_single_subdomain(subdomain):
    return Subdomains.objects(subdomain=subdomain).first()


def get_subdomains(
    program=None,
    scope=None,
    provider=None,
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
    if provider:
        filters["providers"] = [provider]
    if fresh:
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        filters["created_date__gte"] = twenty_four_hours_ago
    print(filters)

    subdomains = Subdomains.objects(**filters)
    if count:
        return subdomains.count()

    if limit is not None and page is not None:
        offset = (page - 1) * limit
        subdomains = subdomains.skip(offset).limit(limit)

    return subdomains
