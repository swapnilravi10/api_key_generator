from django.db import models

# Create your models here.


class API_key_Model(models.Model):
	api_key = models.CharField(max_length=64)
	in_use = models.BooleanField()
	updated_at = models.DateTimeField()

	def __str__(self):
		return self.api_key