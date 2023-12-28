from django.urls import re_path

from investment_report.views import utils

urlpatterns = [
    re_path(
        'preview/(?P<lang>[\w-]+)/(?P<market>[\w-]+)/(?P<sector>[\w-]+)/pdf',
        utils.investment_report_pdf,
        {'moderated': False},
        name='preview_investment_report_pdf',
    ),
    re_path(
        'current/(?P<lang>[\w-]+)/(?P<market>[\w-]+)/(?P<sector>[\w-]+)/pdf',
        utils.investment_report_pdf,
        name='investment_report_pdf',
    ),
    re_path(
        'preview/(?P<lang>[\w-]+)/(?P<market>[\w-]+)/(?P<sector>[\w-]+)/html',
        utils.investment_report_html,
        {'moderated': False},
        name='investment_report_html',
    ),
    re_path(
        'current/(?P<lang>[\w-]+)/(?P<market>[\w-]+)/(?P<sector>[\w-]+)/html',
        utils.investment_report_html,
        {'moderated': True},
        name='investment_report_html',
    ),
    re_path('pir_csv', utils.pir_csv, name='pir_csv'),
    re_path('devcss.css', utils.dev_css, name='dev_css'),
    re_path('devcsslast.css', utils.dev_css_last, name='last_dev_css'),
    re_path('devcssplain.css', utils.dev_css_plain, name='plain_dev_css'),
]
