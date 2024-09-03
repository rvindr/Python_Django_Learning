from rest_framework import serializers
from .models import ExpenseModel

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseModel
        fields = '__all__'

