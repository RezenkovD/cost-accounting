import io

import jinja2
import pdfkit

from datetime import datetime
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

from app import schemas
from app.config import settings
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


@router.get("/user-history/")
def pdf_convertation_user_history(
    filter_date: str = None,
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

    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF)

    pdf_file = pdfkit.from_string(
        output,
        False,
        configuration=config,
        css="templates/static/style.css",
        options={"enable-local-file-access": ""},
    )
    bytes_file = io.BytesIO(pdf_file)

    return StreamingResponse(
        bytes_file,
        headers={"Content-Disposition": 'attachment; filename="my-history.pdf"'},
        media_type="application/pdf",
    )
