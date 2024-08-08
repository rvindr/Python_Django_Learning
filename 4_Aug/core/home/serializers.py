from rest_framework import serializers
from home.models import Person, Color
from django.contrib.auth.models import User

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']


class PersonSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    # custom methods
    # color_info = serializers.SerializerMethodField()

    # def get_color_info(self, obj):
    #     color_objs = Color.objects.get(id = obj.color.id)

    #     return {
    #         'color' : color_objs.color_name,
    #         'hex_code' : '#20232'
    #     }


    class Meta:
        model = Person
        fields = '__all__'
        # depth = 1

    def validate(self, data):

        special_char = "!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        if any(c in special_char for c in data['name']):
            raise serializers.ValidationError('Name must not have special char')

        if data['age'] < 18:
            raise serializers.ValidationError('Age should be greater than 18')

    # def validate_age(self, age):
    #    if age < 18:
    #       raise serializers.ValidationError('Age should be greater than 18')


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField() 


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField() 

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError("username already taken")
            
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError("email already taken")
            
        return data
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        return validated_data