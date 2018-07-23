from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse

from investment_report.metadata import RelatedFieldMetadata
from investment_report.serializers import PIRSerializer
from investment_report.tasks import create_pdf, send_default_investment_email


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


#   XXX Currently index and retrieve endpoint's are not being used anywhere
#   and probably pose a security risk more than anything. Commenting out as
#   this could be useful, and not entirely sure if I should remove entirely
#
#   def get(self, request, identifier=None):
#       if identifier:
#           try:
#               request = PIRRequest.objects.get(id=identifier)
#           except PIRRequest.ObjectDoesNotExist:
#               return Response({'error': 'object not found'}, status=404)

#           serializer = PIRSerializer(request)
#           return Response(serializer.data)

#       else:
#           requests = PIRRequest.objects.all()
#           serializer = PIRSerializer(requests, many=True)
#           return Response(serializer.data)
