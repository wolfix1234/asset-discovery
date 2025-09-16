from fastapi import APIRouter, Query, HTTPException, Request
from fastapi.responses import PlainTextResponse
from typing import Optional
from database.selectors import (
    get_http_services,
    get_single_http_service,
    get_techs,
)

router = APIRouter()


@router.get("/api/subdomains/http", tags=["HTTP"])
async def http_services(
    program: Optional[str] = Query(None),
    scope: Optional[str] = Query(None),
    provider: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    tech: Optional[str] = Query(None),
    fresh: Optional[bool] = Query(False),
    latest: Optional[bool] = Query(False),
    count: Optional[bool] = Query(False),
    limit: Optional[int] = Query(1000),
    page: Optional[int] = Query(1),
    json: Optional[bool] = Query(False),
):
    # Fetch the subdomains based on the provided filters
    http = get_http_services(
        program=program,
        scope=scope,
        provider=provider,
        title=title,
        status=status,
        tech=tech,
        fresh=fresh,
        latest=latest,
        count=count,
        limit=limit,
        page=page,
    )

    # If the
    if count:
        return {"count": http}

    # If no http are found, raise a 404 error
    if not http:
        raise HTTPException(status_code=404, detail="No HTTP service found")

    # Return the response in JSON format if requested
    if json:
        result = [obj.json() for obj in http]
        return result

    # Otherwise, return the response as plain text
    response = "\n".join([f"{obj.subdomain}" for obj in http])
    return PlainTextResponse(response)


@router.get("/api/subdomains/http/details/{subdomain}", tags=["HTTP"])
def get_http_service_detail(subdomain: str):

    http_obj = get_single_http_service(subdomain=subdomain)

    if http_obj:
        return http_obj.json()

    raise HTTPException(
        status_code=404, detail=f"Did not found an HTTP service for {subdomain}"
    )


@router.get("/api/technologies", tags=["Technologies"])
async def get_technologies():
    techs = get_techs()
    response = "\n".join([f"{obj}" for obj in techs])
    return PlainTextResponse(response)
