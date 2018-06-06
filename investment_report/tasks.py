from celery import shared_task


@shared_task
def create_pdf(pir_request_id):
    from investment_report.models import PIRRequest
    instance = PIRRequest.objects.get(id=pir_request_id)
    instance.create_pdf()
