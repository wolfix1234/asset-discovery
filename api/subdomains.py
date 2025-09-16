from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import PlainTextResponse
from typing import Optional
from database.selectors import get_subdomains, get_single_subdomain

router = APIRouter()


@router.get("/api/subdomains", tags=["Subdomains"])
async def subdomains(
    program: Optional[str] = Query(None),
    scope: Optional[str] = Query(None),
    provider: Optional[str] = Query(None),
    fresh: Optional[bool] = Query(False),
    count: Optional[bool] = Query(False),
    limit: Optional[int] = Query(1000),
    page: Optional[int] = Query(1),
    json: Optional[bool] = Query(False),
):
    # Fetch the subdomains based on the provided filters
    subdomains = get_subdomains(
        program=program,
        scope=scope,
        provider=provider,
        fresh=fresh,
        count=count,
        limit=limit,
        page=page,
    )

    # If the count flag is set, return the count instead of the subdomains
    if count:
        return {"count": subdomains}

    # If no subdomains are found, raise a 404 error
    if not subdomains:
        raise HTTPException(status_code=404, detail="No subdomains found")

    # Return the response in JSON format if requested
    if json:
        result = [obj.json() for obj in subdomains]
        return result

    # Otherwise, return the response as plain text
    response = "\n".join([f"{obj.subdomain}" for obj in subdomains])
    return PlainTextResponse(response)


@router.get("/api/subdomains/details/{subdomain}", tags=["Subdomains"])
def get_subdomain_detail(subdomain: str):

    subdomain_obj = get_single_subdomain(subdomain=subdomain)

    if subdomain_obj:
        return subdomain_obj.json()

    raise HTTPException(status_code=404, detail=f"Not found")
