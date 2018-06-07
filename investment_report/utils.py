import glob
import os
import base64
import datetime
import copy
import functools
import weasyprint

from django_countries import data
from countries_plus.models import Country
from io import BytesIO
from PyPDF2 import PdfFileMerger

from bs4 import BeautifulSoup

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import translation
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Q

from investment_report.models import *
from investment_report.markdown import CustomFootnoteExtension, custom_markdown

from moderation.models import MODERATION_STATUS_PENDING

SECTION_KEYS = [
    'front_page', 'sector_overview', 'killer_facts', 'macro_context',
    'uk_market_overview', 'uk_business_info', 'uk_geo_overview',
    'talent_and_education_by_sector',
    'network_and_support', 'sector_initiatives', 'r_and_d_and_innovation', 
    'who_is_here', 'r_and_d_and_innovation_case_study', 'video_case_study', 
    'services_offered_by_dit', 'contact',
]

def filter_translations_and_moderation(klass, **kwargs):
    """
    Filters a model by the currently active translation and
    moderation state.


    I'd normally be using a manager for this, but the
    querysets are fucked with translations

    Everything here takes place within the django lanauge context.
    """

    # Model kwargs used to exclude models if the translation
    # hasn't been added.

    lang = translation.get_language()

    query_params = []

    # Generate exclude kwargs that exclude models that don't
    # have translations.
    for f in klass.TRANSLATION_FIELDS:
        exact = '{}_{}__exact'.format(f, lang)
        isnull = '{}_{}__isnull'.format(f, lang)

        q_exact = Q(**{exact: ''})
        q_isnull = Q(**{isnull: True})

        q = q_exact | q_isnull

        query_params.append(q)

    moderated = kwargs.pop('moderated', True)

    if moderated:
        return klass.objects.exclude(*query_params).filter(**kwargs).first()
    else:
        obj = klass.unmoderated_objects.exclude(
            *query_params
        ).filter(**kwargs).first()

        # Unmoderated objects means something's in the queue
        if obj:
            try:
                return obj.moderated_object.changed_object
            except ObjectDoesNotExist:
                # Happens if object isn't registered with moderation
                return obj
            else:
                # This will happen if the object isn't registered with the moderation
                # system
                return obj
        else:
            return klass.objects.exclude(*query_params).filter(**kwargs).first()


def get_investment_report_data(market, sector, company_name=None, moderated=True):
    context = {}

    filter_ = functools.partial(filter_translations_and_moderation, moderated=moderated)

    context['front_page'] = filter_(
        FrontPage, sector=sector
    )

    context['sector_overview'] = filter_(
        SectorOverview, sector=sector
    )

    context['killer_facts'] = filter_(
        KillerFacts, sector=sector
    )

    context['macro_context'] = filter_(
        MacroContextBetweenCountries, market=market
    )

    context['uk_market_overview'] = filter_(UKMarketOverview)
    context['uk_business_info'] = filter_(UKBusinessInfo)
    context['uk_geo_overview'] = filter_(UKGeographicOverview)

    context['talent_and_education_by_sector'] = filter_(
        TalentAndEducationBySector, sector=sector
    )

    context['network_and_support'] = filter_(
        NetworkAndSupport,
        sector=sector
    )

    context['sector_initiatives'] = filter_(
        SectorInitiatives, sector=sector
    )

    context['r_and_d_and_innovation'] = filter_(
        RDandInnovation, sector=sector
    )

    context['r_and_d_and_innovation_case_study'] = filter_(
        RDandInnovationCaseStudy, sector=sector
    )

    context['video_case_study'] = filter_(
        VideoCaseStudy, sector=sector
    )

    context['services_offered_by_dit'] = filter_(ServicesOfferedByDIT)
    context['contact'] = filter_(Contact)

    context['sector'] = sector.name.title()

    context['who_is_here'] = filter_(
        WhoIsHere
    )

    if company_name:
        context['company'] = company_name

    context['last_page'] = LastPage.objects.first()
    context['settings'] = settings


    context['market_logos'] = MarketLogo.objects.filter(market=market)[:4]
    context['sector_logos'] = SectorLogo.objects.filter(sector=sector)[:4]

    return context


def investment_report_html_generator(market, sector, company_name=None, local=True, moderated=True):
    context = get_investment_report_data(market, sector, company_name, moderated)
    context['local'] = local

    result_html = render_to_string('investment_report.html', context=context)
    last_page_html = render_to_string('investment_report_last_page.html', context=context)

    result_html = (
        result_html
            .replace('$SECTOR', sector.name.title())
            .replace('$MARKET', market.name.title())
    )

    if company_name:
        result_html = result_html.replace('$COMPANY', company_name)

    return (result_html, last_page_html)


def investment_report_pdf_generator(*args, **kwargs):
    """
    Render the (two) html files generated by investment_report_html_generator

    This needs to happen seperately due to constraints in weasyprint.
    
    :params - same as investment_report_html_generator
    :return BytesIO - containing pdf
    """
    pages = investment_report_html_generator(*args, **kwargs)

    files = []
    for p in pages:
        _file = BytesIO()
        weasyprint.HTML(string=p).write_pdf(_file)
        files.append(_file)

    merger = PdfFileMerger()

    for f in files:
        merger.append(f)

    pdf = BytesIO()
    merger.write(pdf)

    for f in files:
        f.close()

    pdf.seek(0)

    return pdf


def send_investment_email(pir_report):
    message_text = render_to_string('pir_email.txt', context={'report': pir_report})
    message_html = render_to_string('pir_email.html', context={'report': pir_report})

    send_mail(
        'Personalised investment report',
        message_text,
        settings.DEFAULT_FROM_EMAIL,
        [pir_report.email],
        fail_silently=False,
        html_message=message_html
    )


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
