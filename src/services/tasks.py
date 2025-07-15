from celery import shared_task

from src.services.email import send_email_activate


@shared_task
def send_email_task(email: str):
    return send_email_activate(email)
