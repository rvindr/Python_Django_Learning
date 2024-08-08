from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model  =Todo
        fields = ['todo_title','todo_description']
        # exclude = ['created_at']

    def validate(self, validated_data):
        if validated_data.get('todo_title'):
            pass