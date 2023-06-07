from starlette.middleware.cors import CORSMiddleware


from fastapi import FastAPI

app = FastAPI()

from app.api.api_v1.router import api_router

app.include_router(api_router, prefix="/api/v1", tags=["v1"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return "This is the root of the Records api, to access documentation go to /docs"

