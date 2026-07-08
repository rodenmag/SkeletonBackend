# document/tasks.py
from celery import shared_task
#from django.db import transaction
#from pdf2image import convert_from_path
#import pdfplumber
#import pytesseract

from .models import Document
import logging
logger = logging.getLogger(__name__)


@shared_task()
def extract_document_text_async():
    logger.info("🔥 extract_document_text_async started")
    logger.info(f"welcome")

"""
@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 10})
def extract_document_text_async(self, document_id):
    doc = Document.objects.get(id=document_id)
    path = doc.file.path

    text_parts = []

    if doc.scanned:
        # OCR path (slow)
        images = convert_from_path(path, dpi=200)

        for img in images[:50]:  # safety limit
            page_text = pytesseract.image_to_string(img)
            if page_text.strip():
                text_parts.append(page_text)

    else:
        # Text-based PDF path (fast)
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages[:100]:
                page_text = page.extract_text(layout=False)
                if page_text:
                    text_parts.append(page_text)

    doc.content_text = "\n".join(text_parts)
    doc.save(update_fields=["content_text"])
"""