from django.shortcuts import render, redirect
from django.utils import translation

from investment_report.models import PIRRequest
from investment_report.forms import PIRForm
from investment_report.utils import investment_report_pdf_generator


def investment_report_form(request):
    if request.method == "POST":
        form = PIRForm(request.POST)

        if form.is_valid():
            pir_request = PIRRequest(**form.cleaned_data)
            pir_request.save()
            pir_request.create_pdf()
            request.session['pir_request'] = pir_request.id
            return redirect('pir_download')

        else:
            return render(request, 'pir_form.html', context={
                'form': form
            })

    return render(request, 'pir_form.html', context={
        'form': PIRForm()
    })


def investment_report_download(request):
    if 'pir_request' not in request.session:
        return redirect('pir')

    pir_request = PIRRequest.objects.get(id=request.session['pir_request'])

    return render(request, 'pir_download.html', context={
        'download_link': pir_request.pdf.url,
        'email': pir_request.email
    })
