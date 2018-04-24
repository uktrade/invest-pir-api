from django.conf.urls import url

from investment_report import views

urlpatterns = [
    url('(?P<lang>[\w-]+)/(?P<market>[\w-]+)/(?P<sector>[\w-]+)/pdf',
        views.investment_report_pdf, name='investment_report_pdf'),

    url('(?P<lang>[\w-]+)/(?P<market>[\w-]+)/(?P<sector>[\w-]+)/html',
        views.investment_report_html, name='investment_report_html'),
]
