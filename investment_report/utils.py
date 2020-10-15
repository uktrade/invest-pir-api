import datetime
import functools
import weasyprint

from io import BytesIO
from PyPDF2 import PdfFileMerger

from django.conf import settings
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import translation

from investment_report import models

from notifications_python_client.notifications import NotificationsAPIClient


def filter_translations_and_moderation(klass, **kwargs):
    """
    Filters a model by the currently active translation and
    moderation state.


    I'd normally be using a manager for this, but the
    querysets are not working because of translations

    Everything here takes place within the django langauge context.
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
        ).filter(**kwargs)

        # Unmoderated objects means something's in the queue
        if obj:
            try:
                if not hasattr(klass, 'MULTI_PAGE'):
                    obj = obj.first()
                    return obj.moderated_object.changed_object
                else:
                    obj = obj.order_by('sub_page')
                    return [
                        _obj.moderated_object.changed_object for _obj in obj
                    ]
            except ObjectDoesNotExist:
                # Happens if object isn't registered with moderation
                return obj
        else:

            obj = klass.objects.exclude(
                *query_params).filter(
                **kwargs)
            if not hasattr(klass, 'MULTI_PAGE'):
                obj = obj.first()
            return obj


class PageCounter:
    def __init__(self, init_value):
        self._index = init_value

    def page(self):
        out = self._index
        self._index += 1
        return out


def get_investment_report_data(
        market,
        sector,
        company_name=None,
        moderated=True):
    context = {
        'page_counter': PageCounter(1)
    }

    filter_ = functools.partial(
        filter_translations_and_moderation,
        moderated=moderated)

    context['lang'] = translation.get_language()

    context['front_page'] = filter_(
        models.FrontPage, sector=sector
    )

    context['sector_overview'] = filter_(
        models.SectorOverview, sector=sector
    )

    context['killer_facts'] = filter_(
        models.KillerFacts, sector=sector
    )

    context['macro_context'] = filter_(
        models.MacroContextBetweenCountries, market=market
    )

    context['uk_market_overview'] = filter_(models.UKMarketOverview)
    context['uk_business_info'] = filter_(models.UKBusinessInfo)

    context['uk_geo_overview'] = filter_(models.UKGeographicOverview)

    context['talent_and_education_by_sector'] = filter_(
        models.TalentAndEducationBySector, sector=sector
    )

    context['network_and_support'] = filter_(
        models.NetworkAndSupport,
        sector=sector
    )

    context['sector_initiatives'] = filter_(
        models.SectorInitiatives, sector=sector
    )

    context['r_and_d_and_innovation'] = filter_(
        models.RDandInnovation, sector=sector
    )

    # context['r_and_d_and_innovation_case_study'] = filter_(
    #     models.RDandInnovationCaseStudy, sector=sector
    # )

    # context['video_case_study'] = filter_(
    #     models.VideoCaseStudy, sector=sector
    # )

    context['services_offered_by_dit'] = filter_(models.ServicesOfferedByDIT)
    context['contact'] = filter_(models.Contact)

    context['sector'] = sector.display_name

    # context['who_is_here'] = filter_(
    #     models.WhoIsHere
    # )
    context['smart_workforce'] = filter_(models.SmartWorkforceSector, sector=sector)
    context['case_study'] = filter_(models.CaseStudySector, sector=sector)
    context['how_we_can_help'] = filter_(models.HowWeCanHelp)

    if company_name:
        context['company'] = company_name

    context['last_page'] = models.LastPage.objects.first()
    context['settings'] = settings

    context['market_logos'] = models.MarketLogo.objects.filter(
        market=market
    )[:4]
    context['sector_logos'] = models.SectorLogo.objects.filter(
        sector=sector
    )[:4]

    context['section_counter'] = 1
    context['current_year'] = datetime.date.today().year

    return context


def investment_report_html_generator(
        market,
        sector,
        company_name=None,
        local=True,
        moderated=True,
        plain=False):
    context = get_investment_report_data(
        market, sector, company_name, moderated)
    context['local'] = local
    if plain:
        template_file = 'investment_report_plain.html'
        last_page_file = 'investment_report_last_page_plain.html'
    else:
        template_file = 'investment_report.html'
        last_page_file = 'investment_report_last_page.html'
    result_html = render_to_string(template_file, context=context)
    last_page_html = render_to_string(
        last_page_file,
        context=context)

    result_html = (
        result_html
        .replace('$SECTOR', sector.display_name)
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

    # Don't generate pdfs locally

    kwargs['local'] = False
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
    notifications_client = NotificationsAPIClient(settings.GOV_NOTIFY_API_KEY)
    notifications_client.send_email_notification(
        email_address=pir_report.email,
        template_id=settings.EMAIL_UUID,
        personalisation={
            'name': pir_report.name,
            'pir_url': pir_report.pdf.url
        }
    )


def send_default_investment_email(pir_report):
    notifications_client = NotificationsAPIClient(settings.GOV_NOTIFY_API_KEY)
    notifications_client.send_email_notification(
        email_address=pir_report.email,
        template_id=settings.DEFAULT_EMAIL_UUID,
        personalisation={
            'name': pir_report.name,
        }
    )
