import requests
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET
from decouple import config


def search(request):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' \
          + request.GET.get('query') + '&key=' + config('GOOGLE_API_KEY')
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return JsonResponse({'response': response.json()})
