from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from database.selectors import get_all_programs, delete_prg

router = APIRouter()


@router.get("/api/programs/all", tags=["Programs"])
async def all_programs():
    programs = get_all_programs()
    response = {program.program_name: program.json() for program in programs}
    return response


@router.delete("/api/programs/{program_name}", tags=["Programs"])
async def delete_program(program_name: str):
    result = delete_prg(program_name=program_name)

    if result == 0:
        raise HTTPException(
            status_code=404, detail=f"Program '{program_name}' not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
