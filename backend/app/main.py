from fastapi import FastAPI
from api.v1.router import api_router
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")


origins = settings.CLIENT_ORIGIN
#origins = ["localhost:8000"]
app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/api/healthcheck")
def root():
    return {"massage": "Server is running"}
