from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from investment_report.metadata import RelatedFieldMetadata
from investment_report.serializers import PIRSerializer
from investment_report.models import PIRRequest


class PIRAPI(APIView):
    serializer_class = PIRSerializer
    metadata_class = RelatedFieldMetadata

    def get_serializer(self, *args):
        return PIRSerializer()

    def post(self, request):
        serializer = PIRSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.instance.create_pdf()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        requests = PIRRequest.objects.all()
        serializer = PIRSerializer(requests, many=True)
        return Response(serializer.data)
