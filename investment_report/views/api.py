import logging

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse

from investment_report.metadata import RelatedFieldMetadata
from investment_report.serializers import PIRSerializer
from investment_report.tasks import create_pdf, send_default_investment_email

logger = logging.getLogger('pir')


class PIRAPI(APIView):
    serializer_class = PIRSerializer

    # Provide OPTIONS data for front end form to work with.
    # Normal related fields don't give options.
    metadata_class = RelatedFieldMetadata

    def get_serializer(self, *args):
        # Done to get RelatedFieldMetadata to work correctly
        return PIRSerializer()

    def post(self, request):
        serializer = PIRSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            if serializer.instance.sector.name == 'other':
                # If 'other' sector send default email
                send_default_investment_email.delay(serializer.instance.id)
            else:
                create_pdf.delay(serializer.instance.id)

            resp = Response(serializer.data, status=201)

            resp['Location'] = reverse(
                'pir_api_detail', args=[serializer.instance.id],
                request=request
            )

            return resp

        # Invalid serializer
        return Response(serializer.errors, status=400)

    def options(self, request, *args, **kwargs):
        logger.critical(request)
        response = super().options(request)
        logger.critical(response)
        return response
