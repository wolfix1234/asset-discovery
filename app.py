from fastapi import FastAPI
from api.lives import router as lives_router
from api.programs import router as programs_router
from api.subdomains import router as subdomains_router
from api.http import router as http_router

app = FastAPI()

app.include_router(lives_router)
app.include_router(programs_router)
app.include_router(subdomains_router)
app.include_router(http_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
