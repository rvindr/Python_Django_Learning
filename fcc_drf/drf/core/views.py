from .serializers import ContactSerializer
from rest_framework import views, status
from rest_framework.response import Response
from core.models import Contact


class ContactAPIView(views.APIView):
    """
    A simple APIView for creating contact entires.
    """
    # serializer_class = ContactSerializer

    # def get_serializer_context(self):
    #     return {
    #         'request': self.request,
    #         'format': self.format_kwarg,
    #         'view': self
    #     }

    # def get_serializer(self, *args, **kwargs):
    #     kwargs['context'] = self.get_serializer_context()
    #     return self.serializer_class(*args, **kwargs)

    def get(self, request):
        data = Contact.objects.all()

        serializer = ContactSerializer(data, many=True)

        return Response({
            'data':serializer.data,
            'message':'data fetched successfully'
        })

    def post(self, request):
        try:
            data = request.data
            serializer = ContactSerializer(data=data)
            
            if not serializer.is_valid():
                return Response({
                    'status':False,
                    'error':serializer.errors
                },status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'status':True,
                'data':serializer.data
            },status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status':False,
                'error': str(e)
            },status=status.HTTP_400_BAD_REQUEST)