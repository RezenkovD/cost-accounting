from fastapi import FastAPI
import routers

app = FastAPI()

app.include_router(routers.users.router)
app.include_router(routers.items.router)
app.include_router(routers.categories.router)
app.include_router(routers.statistics.router)
