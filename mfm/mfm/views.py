from django.db.models import Count, Sum, Min, F, Max, Q, Case, When, IntegerField
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from mfm import settings
import vk
import time
import logging

log = logging.getLogger('view')

def get_first_audio(request):
	time_limit = request.GET.get('time_limit', 200)
	timeout = request.GET.get('timeout', 10)
	query_string = request.GET.get('query')
	session = vk.Session(access_token=settings.VK_AUDIO_TOKEN)
	api = vk.API(session)
	time_start = time.time()
	url = None
	while time.time() - time_start < time_limit:
		try:
			audio_list = api.audio.search(q=query_string)
		except Exception as exception:
			time.sleep(timeout)
		else:
			if len(audio_list):
				url = audio_list[1].get('url') 
				return HttpResponseRedirect(url)
			else:
				HttpResponse(None)



