from home.models import Person, Color
from rest_framework import serializers
from django.contrib.auth.models import User

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']

class PersonSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    class Meta:
        model = Person
        fields = '__all__'


    def validate(self, data):

        special_char = "!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        if any(c in special_char for c in data['name']):
            raise serializers.ValidationError('Name must not have special char')

        if data['age'] < 18:
            raise serializers.ValidationError('Age should be greater than 18')

        return data
    
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):

        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('Username already taken')
        if data['email']:
            if User.objects.filter(username = data['email']).exists():
                raise serializers.ValidationError('email already taken')
            
        return data
    
    def create(self, validated_data):
        user = User.objects.create(username =validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        return validated_data
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()