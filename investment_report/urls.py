from django.conf.urls import url

from investment_report import views

urlpatterns = [
    url('(?P<market>[\w-]+)/(?P<sector>[\w-]+)/',
        views.investment_report),
]
