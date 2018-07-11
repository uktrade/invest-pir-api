from celery import shared_task


@shared_task
def create_pdf(pir_request_id):
    from investment_report.models import PIRRequest
    instance = PIRRequest.objects.get(id=pir_request_id)
    instance.create_pdf()


@shared_task
def send_default_investment_email(pir_request_id):
    from investment_report.models import PIRRequest
    from investment_report.utils import (
        send_default_investment_email as send_email
    )

    instance = PIRRequest.objects.get(id=pir_request_id)
    send_email(instance)
