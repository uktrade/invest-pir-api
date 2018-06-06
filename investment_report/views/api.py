from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from investment_report.metadata import RelatedFieldMetadata
from investment_report.serializers import PIRSerializer
from investment_report.models import PIRRequest
from investment_report.tasks import create_pdf


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

            create_pdf.delay(serializer.instance.id)

            return Response(serializer.data)

        # Invalid serializer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        requests = PIRRequest.objects.all()
        serializer = PIRSerializer(requests, many=True)
        return Response(serializer.data)
