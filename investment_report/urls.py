from functools import partial
from django.conf.urls import url

from investment_report.views import utils

urlpatterns = [
    url('preview/(?P<lang>[\w-]+)/(?P<market>[\w-]+)/(?P<sector>[\w-]+)/pdf',
        utils.investment_report_pdf, {'moderated': False}, name='preview_investment_report_pdf'),

    url('current/(?P<lang>[\w-]+)/(?P<market>[\w-]+)/(?P<sector>[\w-]+)/pdf',
        utils.investment_report_pdf, name='investment_report_pdf'),

    url('preview/(?P<lang>[\w-]+)/(?P<market>[\w-]+)/(?P<sector>[\w-]+)/html',
        utils.investment_report_html, {'moderated': False}, name='investment_report_html'),

    url('current/(?P<lang>[\w-]+)/(?P<market>[\w-]+)/(?P<sector>[\w-]+)/html',
        utils.investment_report_html, {'moderated': True}, name='investment_report_html'),

    url('pir_csv', utils.pir_csv, name='pir_csv')
]
