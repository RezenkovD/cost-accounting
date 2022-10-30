from fastapi import FastAPI
from routers import users, items

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
