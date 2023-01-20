from datetime import datetime

from celery.result import AsyncResult
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse, StreamingResponse
from starlette.templating import Jinja2Templates
from typing import Optional
import jinja2

from app import schemas
from app.celery_app.tasks import pdf_convertation_user_history
from app.crud import crud_statistics
from app.crud.crud_item import read_items_for_user
from app.crud.crud_user import get_current_active_user
from app.db import get_db
from app.utils import transform_date_or_422

router = APIRouter(
    prefix="/pdf-convertation",
    tags=["pdf-convertation"],
)

templates = Jinja2Templates(directory="templates")


@router.get("/{task_id}/")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    return StreamingResponse(
        task_result.result,
        headers={"Content-Disposition": 'attachment; filename="my-history.pdf"'},
        media_type="application/pdf",
    )


@router.post("/")
async def pdf_convert(
    filter_date: Optional[str],
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if filter_date is not None:
        date_ = transform_date_or_422(filter_date)
        data_user_stats = crud_statistics.get_user_statistics(
            db, current_user.id, date_
        )
        list_items = read_items_for_user(db, current_user, date_)
    else:
        data_user_stats = crud_statistics.get_user_statistics(db, current_user.id)
        list_items = read_items_for_user(db, current_user)

    data_user_stats = data_user_stats.__dict__
    today_date = {"today_date": datetime.today().strftime("%d %b, %Y")}

    data_user_stats.update(today_date)
    data_user_stats.update({"items": list_items})

    template_loader = jinja2.FileSystemLoader("templates/")
    template_env = jinja2.Environment(loader=template_loader)
    html_template = "user-history-template.html"
    template = template_env.get_template(html_template)
    output = template.render(data_user_stats)

    task = pdf_convertation_user_history.delay(output)

    return JSONResponse({"task_id": task.id})
