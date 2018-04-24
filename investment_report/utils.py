import glob
import os
import base64
import datetime
import copy

from django_countries import data
from countries_plus.models import Country

from bs4 import BeautifulSoup

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import translation

from investment_report.models import *
from investment_report.markdown import CustomFootnoteExtension, custom_markdown

SECTION_KEYS = [
    'front_page', 'sector_overview', 'killer_facts', 'macro_context',
    'uk_market_overview', 'uk_business_info', 'uk_geo_overview',
    'talent_and_education_generic', 'talent_and_education_by_sector',
    'network_and_support', 'sector_initiatives', 'r_and_d_and_innovation', 
    'who_is_here', 'r_and_d_and_innovation_case_study', 'video_case_study', 
    'services_offered_by_dit', 'contact',
]

def filter_translations(klass, **kwargs):
    """
    I'd normally be using a manager for this, but the
    querysets are fucked with translations
    """
    query_params = {
        f: '' for f in klass.TRANSLATION_FIELDS
    }

    qs = klass.objects.exclude(**query_params)

    return qs.filter(**kwargs).first()


def get_investment_report_data(market, sector, company_name=None):
    context = {}

    context['front_page'] = filter_translations(
        FrontPage, sector=sector
    )

    context['sector_overview'] = filter_translations(
        SectorOverview, sector=sector
    )

    context['killer_facts'] = filter_translations(
        KillerFacts, sector=sector
    )

    context['macro_context'] = filter_translations(
        MacroContextBetweenCountries, market=market
    )

    context['uk_market_overview'] = filter_translations(UKMarketOverview)
    context['uk_business_info'] = filter_translations(UKBusinessInfo)
    context['uk_geo_overview'] = filter_translations(UKGeographicOverview)

    context['talent_and_education_generic'] = filter_translations(TalentAndEducationGeneric)
    context['talent_and_education_by_sector'] = filter_translations(
        TalentAndEducationBySector, sector=sector
    )

    context['network_and_support'] = filter_translations(NetworkAndSupport)

    context['sector_initiatives'] = filter_translations(
        SectorInitiatives, sector=sector
    )

    context['r_and_d_and_innovation'] = filter_translations(
        RDandInnovation, sector=sector
    )

    context['r_and_d_and_innovation_case_study'] = filter_translations(
        RDandInnovationCaseStudy, sector=sector
    )

    context['video_case_study'] = filter_translations(
        VideoCaseStudy, sector=sector
    )

    context['services_offered_by_dit'] = filter_translations(ServicesOfferedByDIT)
    context['contact'] = filter_translations(Contact)

    context['sector'] = sector.name.title()

    context['who_is_here'] = filter_translations(
        WhoIsHere
    )

    if company_name:
        context['company'] = company_name
        svg_data = context['front_page'].background_image.read()
        context['front_page_svg'] = base64.b64encode(svg_data.replace(b'$COMPANY', company_name.encode('utf8')))

    context['settings'] = settings


    context['market_logos'] = MarketLogo.objects.filter(market=market)[:4]
    context['sector_logos'] = SectorLogo.objects.filter(sector=sector)[:4]

    return context


def investment_report_generator(market, sector, company_name=None, local=True):
    context = get_investment_report_data(market, sector, company_name)
    context['local'] = local

    result_html = render_to_string('investment_report.html', context=context)
    result_html = (
        result_html
            .replace('$SECTOR', sector.name.title())
            .replace('$MARKET', market.name.title())
    )

    if company_name:
        result_html = result_html.replace('$COMPANY', company_name)

    return result_html


def get_countries():
    country_files = glob.glob('investment_report/countries/*.txt')
    countries = {}

    name_to_code = {v:k for k,v in  data.COUNTRIES.items()}

    for file_name in country_files:
        with open(file_name) as f:
            countries[file_name.split('/')[-1][:-4]] = [
                Country.objects.get(iso=name_to_code[a]) for a in f.read().split('\n') if a
            ]

    return countries


def valid_context(context):
    """
    Check context has all the required parts
    """
    ctx = copy.copy(context)
    # These aren't required to generate the PDF
    ctx.pop('market_logos')
    ctx.pop('sector_logos')

    if all(list(ctx.values())):
        return True
    else:
        return False


def available_reports():
    markets = Market.objects.filter(name='china')

    report_by_lang = {}

    for lang in dict(settings.LANGUAGES).keys():
        translation.activate(lang)

        report_options = {}

        for m in markets:

            sectors_availible = []

            sectors = Sector.objects.all()

            for s in sectors:
                if valid_context(
                    get_investment_report_data(m, s)
                ):
                    sectors_availible.append(s.name)

            if sectors_availible:
                report_options[m.name] = sectors_availible

        if report_options:
            report_by_lang[lang] = report_options

    translation.activate(settings.LANGUAGE_CODE)

    return report_by_lang
