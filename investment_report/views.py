import os
import datetime
import json
import shutil

from itertools import product
from hashlib import md5
from collections import namedtuple
from io import BytesIO

from PyPDF2 import PdfFileMerger

from django.template.loader import render_to_string
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.utils import translation
from django.conf import settings


from wsgiref.util import FileWrapper

from investment_report.utils import (
    investment_report_html_generator, available_reports, get_investment_report_data,
    valid_context, investment_report_pdf_generator
)

from investment_report.models import Market, Sector, LastPage, PIRRequest
from investment_report.forms import PIRForm


def investment_report_html(request, lang, market, sector, moderated=True):
    market = get_object_or_404(Market, name=market)
    sector = get_object_or_404(Sector, name=sector)

    lang = request.GET.get('lang')
    if lang:
        translation.activate(lang)

    company = request.GET.get('company', 'You')

    return HttpResponse(
        str(investment_report_html_generator(
            market, sector, company, local=False, moderated=moderated
        )[0])
    )


def investment_report_pdf(request, lang, market, sector, moderated=True):
    response = HttpResponse(content_type='application/pdf')

    market = get_object_or_404(Market, name=market)
    sector = get_object_or_404(Sector, name=sector)
    translation.activate(lang)

    company = request.GET.get('company', 'You')

    pdf_file = investment_report_pdf_generator(
        market, sector, company, local=True, moderated=moderated
    )

    pdf = pdf_file.getvalue()
    pdf_file.close()
    response.write(pdf)

    translation.activate(settings.LANGUAGE_CODE)
    return response


def investment_report_form(request):
    if request.method == "POST":
        form = PIRForm(request.POST)

        if form.is_valid():
            market = form.cleaned_data['market']
            sector = form.cleaned_data['sector']
            company = form.cleaned_data['company']
            email = form.cleaned_data['email']

            # Log request
            PIRRequest.objects.create(**form.cleaned_data)

            pdf_hash = '{}{}{}{}.pdf'.format(
                market.name, sector, company,
                datetime.date.today().isoformat()
            )

            request.session['report'] = {
                'email': email,
                'hash': pdf_hash
            }

            pdf_file = investment_report_pdf_generator(market, sector, company)
            pdf_file.seek(0)
            with open(os.path.join(settings.MEDIA_ROOT, pdf_hash), 'wb') as f:
                shutil.copyfileobj(pdf_file, f, length=131072)
            pdf_file.close()

            return redirect('pir_download')

        else:
            return render(request, 'pir_form.html', context={
                'form': form
            })

    return render(request, 'pir_form.html', context={
        'reports': json.dumps(available_reports()),
        'form': PIRForm()
    })


def investment_report_download(request):
    if 'report' not in request.session:
        return redirect('pir')

    path = os.path.join(settings.MEDIA_URL, request.session['report']['hash'])

    return render(request, 'pir_download.html', context={
        'download_link': path,
        'email': request.session['report']['email']
    })
