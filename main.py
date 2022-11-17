from fastapi import FastAPI
from routers import users, items, categories, statistics

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(categories.router)
app.include_router(statistics.router)
