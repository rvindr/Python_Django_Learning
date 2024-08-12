from django.shortcuts import render
from rest_framework.decorators import APIView
from blog.serializers import BlogSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from blog.models import BlogModel
from django.db.models import Q
from django.core.paginator import Paginator

class PublicView(APIView):

    def get(self, request):
        try:
            blogs = BlogModel.objects.all().order_by('?')

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))
                
            page_number = int(request.GET.get('page', 1))
            paginator = Paginator(blogs, 2)
            total_pages = paginator.num_pages

            serializer = BlogSerializer(paginator.page(page_number), many=True)

            return Response({
                'data': serializer.data,
                'message': 'Blog fetch successfully',
                'total_pages': total_pages,
                'current_page': page_number
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': False,
                'message': 'Something went wrong or invalid page',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

class BlogAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get(self, request):
        blogs = BlogModel.objects.filter(user = request.user)
        if request.GET.get('search'):
            search = request.GET.get('search')

            blogs = blogs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))

        serializer = BlogSerializer(blogs, many = True)

        return Response({
            'data' : serializer.data,
            'message' : 'Blog List fetch successfully'
        }, status=status.HTTP_200_OK)

    def post(self, request):

        try:
            data =request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'status':False,
                    'message':'something went wrong',
                    'data' : serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            return Response({
                'status':True,
                'message':'blog created successfully',
                'data':serializer.data
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:

            return Response({
                    'status':False,
                    'message':'something went wrong',
                    'data':{}
                }, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        try:
            data =request.data
            blog = BlogModel.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                return Response({
                        'data':{},
                        'message':'invalid blog uid'
                    },status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                return Response({
                    'data':{},
                    'message':'you are not authorized to do this'
                },status=status.HTTP_403_FORBIDDEN)
            
            serializer = BlogSerializer(blog[0],data=data, partial =True)
            if not serializer.is_valid():
                return Response({
                    'status':False,
                    'message':'something went wrong',
                    'data' : serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({
                'status':True,
                'message':'blog updated successfully',
                'data':serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:

            return Response({
                    'status':False,
                    'message':'something went wrong',
                    'data':{}
                }, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        try:
            data =request.data
            blog = BlogModel.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                return Response({
                        'data':{},
                        'message':'invalid blog uid'
                    },status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                return Response({
                    'data':{},
                    'message':'you are not authorized to do this'
                },status=status.HTTP_403_FORBIDDEN)
            
            blog[0].delete()

            return Response({
                'status':True,
                'message':'blog deleted successfully',
                'data':{}
            }, status=status.HTTP_200_OK)
        except Exception as e:

            return Response({
                    'status':False,
                    'message':'something went wrong',
                    'data':{}
                }, status=status.HTTP_400_BAD_REQUEST)