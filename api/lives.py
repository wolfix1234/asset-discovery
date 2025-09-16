from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import PlainTextResponse
from typing import Optional
from database.selectors import (
    get_single_subdomain,
    get_single_live,
    get_lives,
)

router = APIRouter()


@router.get("/api/subdomains/live/details/{subdomain}", tags=["Lives"])
def get_live_subdomain_detail(subdomain: str):

    live_obj = get_single_live(subdomain=subdomain)
    subdomain_obj = get_single_subdomain(subdomain=subdomain)

    if live_obj and subdomain_obj:

        return {
            "program_name": live_obj.program_name,
            "subdomain": live_obj.subdomain,
            "scope": live_obj.scope,
            "ips": live_obj.ips or [],
            "tag": live_obj.tag,
            "providers": subdomain_obj.providers or [],
            "created_date": (
                live_obj.created_date.isoformat() if live_obj.created_date else None
            ),
            "last_update": (
                live_obj.last_update.isoformat() if live_obj.last_update else None
            ),
        }

    return f"{subdomain} not found"


@router.get("/api/subdomains/live", tags=["Lives"])
async def live_subdomains(
    program: Optional[str] = Query(None),
    scope: Optional[str] = Query(None),
    provider: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    fresh: Optional[bool] = Query(False),
    count: Optional[bool] = Query(False),
    limit: Optional[int] = Query(1000),
    page: Optional[int] = Query(1),
    json: Optional[bool] = Query(False),
):
    # Fetch the subdomains based on the provided filters
    live_subdomains = get_lives(
        program=program,
        scope=scope,
        provider=provider,
        tag=tag,
        fresh=fresh,
        count=count,
        limit=limit,
        page=page,
    )

    # If the count flag is set, return the count instead of the live_subdomains
    if count:
        return {"count": live_subdomains}

    # If no live_subdomains are found, raise a 404 error
    if not live_subdomains:
        raise HTTPException(status_code=404, detail="No live_subdomains found")

    # Return the response in JSON format if requested
    if json:
        result = [obj.json() for obj in live_subdomains]
        return result

    # Otherwise, return the response as plain text
    response = "\n".join([f"{obj.subdomain}" for obj in live_subdomains])
    return PlainTextResponse(response)

