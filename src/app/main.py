from fastapi import FastAPI

from app.routers.users import router as users_router
from app.routers.items import router as items_router
from app.routers.categories import router as categories_router
from app.routers.statistics import router as statistics_router

app = FastAPI()

app.include_router(users_router)
app.include_router(items_router)
app.include_router(categories_router)
app.include_router(statistics_router)
