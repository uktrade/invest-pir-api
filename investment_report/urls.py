from functools import partial
from django.conf.urls import url

from investment_report import views

urlpatterns = [
    url('preview/(?P<lang>[\w-]+)/(?P<market>[\w-]+)/(?P<sector>[\w-]+)/pdf',
        views.investment_report_pdf, {'moderated': False}, name='preview_investment_report_pdf'),

    url('current/(?P<lang>[\w-]+)/(?P<market>[\w-]+)/(?P<sector>[\w-]+)/pdf',
        views.investment_report_pdf, name='investment_report_pdf'),

    url('(?P<lang>[\w-]+)/(?P<market>[\w-]+)/(?P<sector>[\w-]+)/html',
        views.investment_report_html, name='investment_report_html'),
]
