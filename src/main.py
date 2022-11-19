from fastapi import FastAPI
import src

app = FastAPI()

app.include_router(src.routers.users.router)
app.include_router(src.routers.items.router)
app.include_router(src.routers.categories.router)
app.include_router(src.routers.statistics.router)
