from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        
        if not User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('account not found')
        
        return data
    
    def get_jwt_token(user, data):

        user = authenticate(username = data['username'], password = data['password'])
        if not user:
            return {'message':'invalid credential',
                    'data':{}
                    }
        
        refresh = RefreshToken.for_user(user)

        return {
            'message':'login success',
            'data':{
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }