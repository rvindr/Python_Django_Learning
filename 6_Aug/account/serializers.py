from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('Username already taken')
            
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError('email already registed')
            
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username'].lower(),
            email = validated_data['email'].lower()
        )
        user.set_password(validated_data['password'])
        user.save()

        return validated_data

        
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
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