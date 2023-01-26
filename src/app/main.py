import uvicorn
from fastapi import FastAPI

from app.routers.users import router as users_router
from app.routers.items import router as items_router
from app.routers.categories import router as categories_router
from app.routers.statistics import router as statistics_router
from app.routers.token import router as token_router
from app.routers.pdf_convertations import router as pdf_router
from app.routers.groups import router as group_router
from app.routers.invitations import router as invitation_router
from app.config import settings

app = FastAPI()

app.include_router(users_router)
app.include_router(items_router)
app.include_router(categories_router)
app.include_router(statistics_router)
app.include_router(token_router)
app.include_router(pdf_router)
app.include_router(group_router)
app.include_router(invitation_router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
    )
