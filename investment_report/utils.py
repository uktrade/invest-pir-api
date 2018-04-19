import os
import base64
import datetime

from bs4 import BeautifulSoup

from django.conf import settings
from django.template.loader import render_to_string

from investment_report.models import *
from investment_report.markdown import CustomFootnoteExtension, custom_markdown


def bs_parse(html):
    return BeautifulSoup(html, 'html.parser')


def investment_report_generator(market, sector, company_name, local=True):
    context = {}
    context['local'] = local

    context['sector_overview'] = SectorOverview.objects.filter(
        sector=sector
    ).first()


    context['killer_facts'] = KillerFacts.objects.filter(
        sector=sector
    ).first()

    context['macro_context'] = MacroContextBetweenCountries.objects.filter(
        market=market
    ).first()

    context['uk_market_overview'] = UKMarketOverview.objects.first()
    context['uk_business_info'] = UKBusinessInfo.objects.first()
    context['uk_geo_overview'] = UKGeographicOverview.objects.first()
    context['talent_and_education_generic'] = TalentAndEducationGeneric.objects.first()
    context['network_and_support'] = NetworkAndSupport.objects.first()

    context['talent_and_education_by_sector'] = TalentAndEducationBySector.objects.filter(
        sector=sector
    ).first()

    context['sector_initiatives'] = SectorInitiatives.objects.filter(
        sector=sector
    ).first()

    context['r_and_d_and_innovation'] = RDandInnovation.objects.filter(
        sector=sector
    ).first()

    context['r_and_d_and_innovation_case_study'] = RDandInnovationCaseStudy.objects.filter(
        sector=sector
    ).first()

    context['who_is_here'] = []
    context['video_case_study'] = VideoCaseStudy.objects.filter(
        sector=sector
    ).first()


    context['services_offered_by_dit'] = ServicesOfferedByDIT.objects.first()
    context['call_to_action'] = CallToAction.objects.first()
    context['testimonials'] = Testimonials.objects.first()


    context['contact'] = Contact.objects.first()

    context['sector'] = sector.name.title()
    context['company'] = company_name

    context['front_page'] = FrontPage.objects.filter(
        sector=sector
    ).first()

    context['who_is_here'] = WhoIsHere.objects.first()

    if company_name:
        svg_data = context['front_page'].background_image.read()
        context['front_page_svg'] = base64.b64encode(svg_data.replace(b'$COMPANY', company_name.encode('utf8')))

    context['settings'] = settings


    context['market_logos'] = MarketLogo.objects.filter(market=market)[:4]
    context['sector_logos'] = SectorLogo.objects.filter(market=market)[:4]

    result_html = render_to_string('investment_report.html', context=context)

    result_html = (
        result_html
            .replace('$COMPANY', company_name)
            .replace('$SECTOR', sector.name.title())
            .replace('$MARKET', market.name.title())
    )

    return result_html
