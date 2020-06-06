from rest_framework import serializers
from . models import API_key_Model

class Api_key_serializer(serializers.ModelSerializer):

	class Meta :

		model = API_key_Model
		fields = ('api_key', 'in_use')