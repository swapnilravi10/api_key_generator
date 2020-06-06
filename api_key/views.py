from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from . models import API_key_Model
from rest_framework.response import Response
from . serializers import Api_key_serializer
from  api_key.tasks import keep_alive, release_key	
from rest_framework import status
import random, string
from datetime import datetime, timezone

##API_key generator to generate key on route /generate_key
class API_generator_View(APIView):

	def get(self, request):
		api_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(64))
		key = API_key_Model.objects.create(api_key=api_key, in_use=False, updated_at=datetime.now(timezone.utc))
		key.save()
		return JsonResponse(data={"api_key":api_key})


class API_key_View(APIView):


	def get_unused_key(self):
		keys = API_key_Model.objects.filter(in_use=False).order_by('?').first()
		serializer = Api_key_serializer(keys)
		return serializer
				
	def get(self, request):
		serializer = self.get_unused_key()
		key = serializer.data['api_key']
		if key != "":
			API_key_Model.objects.filter(api_key=key).update(in_use=True, updated_at=datetime.now(timezone.utc))
			
			return JsonResponse(data={"api_key" : key})
		else:
			return JsonResponse(data={"status" : 400, "message":"NOT FOUND"})

	def post(self,request):
		key = request.data["api_key"]
		if API_key_Model.objects.filter(api_key=key).exists():
			API_key_Model.objects.filter(api_key=key).update(in_use=False, updated_at=datetime.now(timezone.utc))
			return JsonResponse(data={"status" : 200, "message":"key unblocked"})
		else:
			return JsonResponse(data={"status" : 404, "message":"Invalid key"})

	"""Blocked keys get released in 60 seconds if unblockkey is not called"""				
	release_key.delay()

	def delete(self,request):
		key = request.data["api_key"]
		api_key = API_key_Model.objects.get(api_key=key)
		try:
			API_key_Model.objects.get(pk=api_key.id).delete()
			return JsonResponse(data={"status" : 200, "message":"key deleted"})

		except API_key_Model.DoesNotExist:
			return JsonResponse(data={"status": 404, "message": "No such key exists"})

	"""If a particular key not not recieved keep_alive in last five  minutes the key is deleted"""
	keep_alive.delay()
		
		