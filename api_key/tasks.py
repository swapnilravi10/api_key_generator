from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery import shared_task
from api_key.models import API_key_Model
from datetime import datetime,timezone

@shared_task
def keep_alive():

	expected_time = 5.0
	keys = API_key_Model.objects.all()
	for key in keys.values('id','updated_at'):
		initial = key['updated_at']
		now = datetime.now(timezone.utc)
		time_diff = now - initial
		minutes = time_diff.seconds / 60
		if minutes > expected_time:
			to_be_deleted = API_key_Model.objects.get(pk=key['id'])
			to_be_deleted.delete()
		else:
			pass


@shared_task
def release_key():

	expected_time = 60
	keys = API_key_Model.objects.filter(in_use=True)
	for key in keys.values('id', 'updated_at'):
		initial = key['updated_at']
		now = datetime.now(timezone.utc)
		time_diff = now - initial
		seconds = divmod(time_diff.seconds , 60)
		sec = int(''.join(map(str, seconds)))
		if sec > expected_time:
			API_key_Model.objects.filter(id=key['id']).update(in_use=False)
			



