#skeleton 

#TODO will do it when i will use kubernetes for now the cody is only composed of ideas for distant future
@app.get("/healthz/liveness", status_code=status.HTTP_200_OK)
def liveness():
    # Sprawdza tylko, czy sam proces Pythona żyje i odpowiada
    return {"status": "alive"}

@app.get("/healthz/readiness")
def readiness(response: Response):
    # Sprawdza, czy aplikacja ma połączenie z bazą danych / zewnętrznym API
    if not check_db_connection():
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unhealthy", "reason": "database unreachable"}
    return {"status": "ready"}


from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: nawiąż połączenia z bazą, zinicjalizuj zasoby
    yield
    # Shutdown: K8s zamyka pod – zamknij poole połączeń
    await database.disconnect()

app = FastAPI(lifespan=lifespan)