from rest_framework import serializers
from core.models import Contact

class ContactSerializer(serializers.ModelSerializer):
	# name = serializers.CharField(source="title", required=True)
	# message = serializers.CharField(source="description", required=True)
	# email = serializers.EmailField(required=True)
	
	class Meta:
		model = Contact
		fields = (
			'name',
			'email',
			'message'
		)