from database.models import Http, Subdomains
from datetime import datetime, timedelta


def get_single_http_service(subdomain):
    return Http.objects(subdomain=subdomain).first()


def get_http_services(
    program=None,
    scope=None,
    provider=None,
    title=None,
    status=None,
    tech=None,
    fresh=False,
    latest=False,
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
        subdomains = Subdomains.objects(providers=[provider])
        sub_urls = [sub.subdomain for sub in subdomains]
        filters["subdomain__in"] = sub_urls
    if title:
        filters["title__icontains"] = title
    if status:
        filters["status_code"] = status
    if tech:
        filters["tech__icontains"] = tech
    if latest:
        twelve_hours_ago = datetime.now() - timedelta(hours=12)
        filters["last_update__gte"] = twelve_hours_ago

    http = Http.objects(**filters)
    if count:
        return http.count()

    if limit is not None and page is not None:
        offset = (page - 1) * limit
        http = http.skip(offset).limit(limit)

    return http


def get_techs():
    return Http.objects.distinct("tech")
