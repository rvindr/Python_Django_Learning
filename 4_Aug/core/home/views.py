from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from home.serializers import PersonSerializer, LoginSerializer, RegisterSerializer
from home.models import Person
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# Create your views here.

class LoginAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status':False,
                'message': 'invalid credential',
                
            }, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        if not user:
            return Response({
                'status':False,
                'message': serializer.errors,
                
            }, status=status.HTTP_400_BAD_REQUEST)
        token,_ = Token.objects.get_or_create(user=user)

        return Response({
            'staus':True,
            'message':'user login',
            'token':str(token)

        }, status=status.HTTP_201_CREATED)
    


class RegisterAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status':False,
                'message': serializer.errors,
                
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({
            'status':True,
            'message':'user created',
        }, status=status.HTTP_201_CREATED)

   


@api_view(['GET','POST'])
def index(request):
    courses = {
        'program' : 'Python',
        'instructor' : 'abhijeet gupta',
        'key_skill' : ['Django', 'flask', 'FastApi'],
        'fees' : 65299
    }

    if request.method == 'GET':
        print(request.GET.get('search'))

        print('You hit a GET method')
        return Response(courses)
    
    if request.method == 'POST':
        print(request.POST.get('search'))
        return Response(courses)

    return Response(courses)


@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    
    if request.method == 'GET':
        persons = Person.objects.filter(color__isnull = False)
        serializer = PersonSerializer(persons, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = PersonSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == 'PUT':
        data = request.data
        serializer = PersonSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == 'PATCH':
        data = request.data
        objs = Person.objects.get(id = data['id'])
        serializer = PersonSerializer(objs, data=data, partial = True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    else:
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()

        return Response({
            'message' : 'person delete'
        })
    
@api_view(['POST'])
def login(request):
    data  = request.data
    serializer = LoginSerializer(data=data)

    if serializer.is_valid():
        serializer.validated_data
        return Response({
            'message' : 'suucessfully login'
        })
    return Response(serializer.errors)

class PersonAPI(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def get(self, request):
       return Response({
            'message' : 'You hit get method'
        })
    
    def put(self, request):
        return Response({
            'message' : 'You hit put method'
        })
    def patch(self, request):
        return Response({
            'message' : 'You hit patch method'
        })
    def post(self, request):
        return Response({
            'message' : 'You hit post method'
        })
    def delete(self, request):
        return Response({
            'message' : 'You hit delete method'
        })
    
class PersonViewSet(viewsets.ModelViewSet):

    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    # http_method_names = ['GET', 'POST']
    def list(self, request):

        search = request.GET.get('search')
        queryset = self.queryset
        
        if queryset:
            queryset = queryset.filter(name__startswith = search)
        
        serializer = PersonSerializer(queryset, many=True)

        return Response({
            'status':200,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
