import markdown

from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from investment_report.models import *
from investment_report.markdown import CustomFootnoteExtension


def bs_parse(html):
    return BeautifulSoup(html, 'html.parser')


def markdown_fragment(a_str):
    return markdown.markdown(a_str, extensions=[CustomFootnoteExtension()])


def investment_report_generator(market, sector):
    context = {}

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
    context['video_case_study'] = {}


    context['services_offered_by_dit'] = ServicesOfferedByDIT.objects.first()
    context['call_to_action'] = CallToAction.objects.first()
    context['testimonials'] = Testimonials.objects.first()

    return render_to_string('investment_report.html', context=context)
