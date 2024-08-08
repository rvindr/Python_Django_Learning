from rest_framework import generics, permissions, authentication
from rest_framework.decorators import APIView
from rest_framework.response import Response
from home.models import Product
from home.serializers import ProductSerializer

# Genericxs Retrieve APIView

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'


class ProductAPI(APIView):
    # session authentication and permission

    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.SessionAuthentication]
    
    def get(self, request):
        objs = Product.objects.filter()

        serializer = ProductSerializer(objs, many=True)

        return Response({
            'status':True,
            'data':serializer.data,
            'message':'product fetch successfully'
        })
    
