from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import translation

from investment_report.utils import investment_report_generator
from investment_report.models import Market, Sector

# Create your views here.
def investment_report(request, market, sector):
    market = get_object_or_404(Market, name=market)
    sector = get_object_or_404(Sector, name=sector)

    lang = request.GET.get('lang')
    if lang:
        translation.activate(lang)

    company = request.GET.get('company')

    return HttpResponse(
        str(investment_report_generator(market, sector, company))
    )
