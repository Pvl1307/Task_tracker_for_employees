from fastapi import FastAPI

from src.core.config import FASTAPI_SETTINGS
from src.routers.employees_routers import router as employees_route
from src.routers.tasks_routers import router as tasks_route

app = FastAPI(**FASTAPI_SETTINGS)

app.include_router(employees_route)
app.include_router(tasks_route)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
