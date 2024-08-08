
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import TodoSerializer
from .models import Todo

@api_view(['GET','POST','PATCH'])
def get_home(request):
    if request.method == 'GET':
        return Response({
            'status':200,
            'message':'Yes! Django rest frameword is working',
            'method_called':'You called Get method'
        })
    elif request.method == 'POST':
        return Response({
            'status':200,
            'message':'Yes! Django rest frameword is working',
            'method_called':'You called Post method'
        })
    elif request.method == 'PATCH':
        return Response({
            'status':200,
            'message':'Yes! Django rest frameword is working',
            'method_called':'You called PATCH method'
        })
    else:
        return Response({
            'status':400,
            'message':'Yes! Django rest frameword is working',
            'method_called':'You called Invalid method'
        })

@api_view(['GET'])
def get_todo(request):
    todos_objs = Todo.objects.all()
    serializer = TodoSerializer(todos_objs,many=True)

    return Response({
        'status':True,
        'message':'Todo fetched',
        'data':serializer.data
    })

@api_view(['POST'])
def post_todo(request):
    try:
        data = request.data
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)

            return Response({
                'status':True,
                'message':serializer.data
            })
        
        return Response({
            'status':False,
            'message':'Invalid data',
            'data':serializer.errors
        })


    except Exception as e:
         return Response({
            'status':False,
            'message':'Something went wrong'
        })