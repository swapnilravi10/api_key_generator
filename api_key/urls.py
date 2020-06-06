from django.urls import path
from . views import API_generator_View, API_key_View

urlpatterns = [
	path('generate_key', API_generator_View.as_view()),
	path('available_key', API_key_View.as_view()),
	path('unblock_key', API_key_View.as_view()),
	path('delete_key', API_key_View.as_view()),
]