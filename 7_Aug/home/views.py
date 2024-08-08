from rest_framework import generics
from rest_framework.decorators import APIView
from home.models import Product
from home.serializers import ProductSerializer

# Genericxs Retrieve APIView

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'



class ProductAPI(APIView):
    pass