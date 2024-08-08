# # this code is from home.views
# from django.shortcuts import render
# from rest_framework.decorators import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from home.models import Product
# from home.serializers import ProductSerializer



# # Create your views here.

# class ProductAPI(APIView):

#     def get(self, request):

#         data = Product.objects.all()

#         serializer = ProductSerializer(data, many=True)

#         return Response({
#             'status' : True,
#             'data' : serializer.data,
#             'message':'product fetch successfully'
#         }, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         try:
#             data = request.data

#             serializer = ProductSerializer(data=data)

#             if not serializer.is_valid():
#                 return Response({
#                     'status':False,
#                     'message':serializer.errors,
#                     'data':{}
#                 }, status=status.HTTP_400_BAD_REQUEST)
#             serializer.save()

#             return Response({
#                 'status':True,
#                 'message':'product added',
#                 'data':serializer.data
#             }, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             print(e)
#             return Response({
#                 'status':False,
#                 'meassage':'something went wrong'
#             }, status=status.HTTP_400_BAD_REQUEST)
        
# # 