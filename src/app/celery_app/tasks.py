import io
import pdfkit

from app.config import settings
from app.celery_app.celery_config import celery_app


@celery_app.task
def pdf_convertation_user_history(output):
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
    pdf_file = pdfkit.from_string(
        output,
        False,
        configuration=config,
        css="/home/riezienkov/projects/cost-accounting/src/app/templates/static/style.css",
        options={"enable-local-file-access": ""},
    )
    bytes_file = io.BytesIO(pdf_file)

    return bytes_file
