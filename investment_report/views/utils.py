from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import translation
from django.conf import settings


from investment_report.utils import (
    investment_report_html_generator, investment_report_pdf_generator
)

from investment_report.models import Market, Sector


def investment_report_html(request, lang, market, sector, moderated=True):
    """
    Used for previewing on dev
    """
    market = get_object_or_404(Market, name=market)
    sector = get_object_or_404(Sector, name=sector)
    company = request.GET.get('company', 'You')
    lang = request.GET.get('lang', settings.LANGUAGE_CODE)

    with translation.override(lang):
        return HttpResponse(
            str(investment_report_html_generator(
                market, sector, company, local=False, moderated=moderated
            )[0])
        )


def investment_report_pdf(request, lang, market, sector, moderated=True):
    """
    Used for previewing on the admin
    """
    market = get_object_or_404(Market, name=market)
    sector = get_object_or_404(Sector, name=sector)
    company = request.GET.get('company', 'You')
    translation.activate(lang)

    with translation.override(lang):
        pdf_file = investment_report_pdf_generator(
            market, sector, company, local=True, moderated=moderated
        )

        pdf = pdf_file.getvalue()
        pdf_file.close()

        response = HttpResponse(content_type='application/pdf')
        response.write(pdf)
        return response
