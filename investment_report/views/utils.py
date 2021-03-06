import csv
import logging

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import translation
from django.contrib.auth.decorators import login_required
from django.conf import settings


from investment_report.utils import (
    investment_report_html_generator, investment_report_pdf_generator
)

from investment_report.models import Market, Sector, PIRRequest


@login_required
def investment_report_html(request, lang, market, sector, moderated=True):
    """
    Used for previewing on dev
    """
    market = get_object_or_404(Market, name=market)
    sector = get_object_or_404(Sector, name=sector)
    company = request.GET.get('company', 'You')

    with translation.override(lang):
        return HttpResponse(
            str(investment_report_html_generator(
                market, sector, company, local=False, moderated=moderated
            )[0])
        )


@login_required
def investment_report_pdf(request, lang, market, sector, moderated=True):
    """
    Used for previewing on the admin
    """
    market = get_object_or_404(Market, name=market)
    sector = get_object_or_404(Sector, name=sector)
    company = request.GET.get('company', 'You')
    plain = request.GET.get('plain', 'false') == 'true'

    with translation.override(lang):
        pdf_file = investment_report_pdf_generator(
            market, sector, company,
            local=True,
            moderated=moderated,
            plain=plain
        )

        pdf = pdf_file.getvalue()
        pdf_file.close()

        response = HttpResponse(content_type='application/pdf')
        response.write(pdf)
        return response


@login_required
def pir_csv(request):

    logging.getLogger('pir-csv-download').info(
        'PIR CSV downloaded by %s',
        request.user.email)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        'attachment; filename="pir_reports_export.csv"'
    )

    fields = [
        'id', 'country', 'market__name', 'sector__name', 'name',
        'lang', 'company', 'email', 'phone_number', 'date_created',
        'gdpr_optin',
    ]

    writer = csv.DictWriter(
        response,
        fieldnames=fields
    )

    writer.writeheader()

    for pir_request in PIRRequest.objects.order_by('id').values(*fields):
        writer.writerow(pir_request)

    return response


def dev_css(request):
    # '/usr/src/app
    with open(
        '{}/investment_report/static/build/investment-report.css'.format(settings.ROOT), 'r'
    ) as css:
        content = css.read()
    response = HttpResponse(content, content_type='text/css')
    return response


def dev_css_plain(request):
    """
    A utility view for testing, to load the live css, instead of a static resource
    """
    with open(
        '{}/investment_report/static/build/investment-report-plain.css'.format(settings.ROOT), 'r'
    ) as css:
        content = css.read()
    response = HttpResponse(content, content_type='text/css')
    return response


def dev_css_last(request):
    """
    A utility view for testing, to load the live last page css, instead of a static resource
    """
    with open(
        '/usr/src/app/investment_report/static/build/investment-report-last-page.css', 'r'
    ) as css:
        content = css.read()
    response = HttpResponse(content, content_type='text/css')
    return response
