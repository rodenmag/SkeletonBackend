# document/tasks.py
from celery import shared_task
from django.db import transaction
from pdf2image import convert_from_path
import re
import pdfplumber
import pytesseract

from .models import *
import logging
logger = logging.getLogger(__name__)

from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings

"""
@shared_task()
def extract_document_text_async():
    logger.info("extract_document_text_async started")
    logger.info(f"welcome")
"""

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

@shared_task
def send_for_approval_notifications(document_id):
    try:
        document = DocumentFile.objects.get(id=document_id)

        approvers = document.approval.all()

        for approver in approvers:
            if not approver.email:
                continue

            message = (
                f"Good Day, {approver.get_full_name() or approver.username},\n\n"
                f"There is a new uploaded document that requires your approval.\n\n"
                f"Subject: {document.subject}\n"
                f"Document Type: {document.document_type}\n"
                f"Date Issued: {document.date_issued}\n"
                f"Document Status: {document.status}\n"
                f"Approval Status: {document.approval_status}\n"
                f"Please login to the QDMS to review the document.\n\n"
                f"Thank you."
            )

            email = EmailMultiAlternatives(
                subject="QDMS - Document Approval Required",
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[approver.email]
            )

            email.send(fail_silently=False)

        return "Emails sent successfully"

    except DocumentFile.DoesNotExist:
        return f"Document {document_id} does not exist"

@shared_task
def activity_post_async(document_id, function, user):

    document = DocumentFile.objects.get(id=document_id)

    activity = Activity.objects.create(
        file_name=document.file.name if document.file else None,
        
        function=function,
        user=user,

        document_type=document.document_type,
        status=document.status,
        subject=document.subject,
        short_description=document.short_description,
        content_text=document.content_text,
        scanned=document.scanned,
        revision_number=document.revision_number,
        board_resolution_number=document.board_resolution_number,
        date_issued=document.date_issued,
        related_board_resolution_number=document.related_board_resolution_number,
        department=document.department,
        approved_by=document.approved_by,
        posted_by=document.posted_by,
        date_posted=document.date_posted,
        time_posted=document.time_posted,
        approval_status=document.approval_status,
        public_viewer=document.public_viewer,

    )

    # copy many-to-many
    activity.approval.set(document.approval.all())
    activity.department_viewer.set(document.department_viewer.all())
    activity.specific_viewer.set(document.specific_viewer.all())
    activity.group_viewer.set(document.group_viewer.all())

    return 'Activity Logged'

@shared_task
def activity_post_delete_async(data):

    department = None

    if data.get('department_id'):
        department = Department.objects.filter(
            id=data['department_id']
        ).first()

    activity = Activity.objects.create(
        function=data.get('function'),
        user=data.get('user'),

        document_type=data.get('document_type'),
        status=data.get('status'),
        subject=data.get('subject'),
        short_description=data.get('short_description'),
        content_text=data.get('content_text'),
        scanned=data.get('scanned'),
        revision_number=data.get('revision_number'),
        board_resolution_number=data.get('board_resolution_number'),
        date_issued=data.get('date_issued'),
        related_board_resolution_number=data.get('related_board_resolution_number'),
        department=department,
        approved_by=data.get('approved_by'),
        posted_by=data.get('posted_by'),
        date_posted=data.get('date_posted'),
        time_posted=data.get('time_posted'),
        approval_status=data.get('approval_status'),
        public_viewer=data.get('public_viewer'),
    )

    activity.approval.set(
        User.objects.filter(id__in=data.get('approval_ids', []))
    )

    activity.department_viewer.set(
        Department.objects.filter(
            id__in=data.get('department_viewer_ids', [])
        )
    )

    activity.specific_viewer.set(
        User.objects.filter(
            id__in=data.get('specific_viewer_ids', [])
        )
    )

    return 'Delete Activity Logged'

# NORMALIZE TEXT
def normalize_text(text):
    if not text:
        return ""

    # Convert all line endings to \n
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove tabs
    text = text.replace("\t", " ")

    # Remove trailing spaces per line
    text = "\n".join(line.strip() for line in text.split("\n"))

    # Remove multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove multiple spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    return text.strip()

# OCR A SINGLE PAGE
def ocr_pdf_page(path, page_number, dpi=200):
    images = convert_from_path(
        path,
        dpi=dpi,
        first_page=page_number + 1,
        last_page=page_number + 1,
    )

    text = pytesseract.image_to_string(images[0])
    return normalize_text(text)


# HYBRID PDF TASK
@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 10},
)

def extract_document_text_async(self, document_id):

    doc = DocumentFile.objects.get(id=document_id)
    path = doc.file.path

    text_parts = []
    text_pages = 0
    ocr_pages = 0

    with pdfplumber.open(path) as pdf:

        total_pages = min(len(pdf.pages), 100)

        for page_index in range(total_pages):

            page = pdf.pages[page_index]

            page_text = page.extract_text(layout=False)

            if page_text and page_text.strip():

                cleaned_text = normalize_text(page_text)

                if cleaned_text:
                    text_parts.append(cleaned_text.replace("\n", " ").replace("\r", " "))

                text_pages += 1

            else:

                ocr_text = ocr_pdf_page(path, page_index)

                if ocr_text:
                    text_parts.append(ocr_text.replace("\n", " ").replace("\r", " "))

                ocr_pages += 1

    full_text = " ".join(text_parts)

    full_text = normalize_text(full_text).replace("\n", " ").replace("\r", " ")

    scanned_only = ocr_pages > 0 and text_pages == 0

    with transaction.atomic():

        doc.content_text = full_text
        doc.scanned = scanned_only

        doc.save(
            update_fields=[
                "content_text",
                "scanned",
            ]
        )