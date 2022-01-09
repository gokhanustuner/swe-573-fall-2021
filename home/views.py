import operator
import socket
import requests
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from services.documents import ServiceDocument, ServiceRateDocument
from elasticsearch_dsl.query import Q
from functools import reduce
from django.views.decorators.cache import never_cache
from decimal import *

@require_GET
@never_cache
@login_required
def feed(request):
    context = {}
    if not request.GET.get('nearby'):
        services = ServiceDocument.search().sort('-start_date')
    else:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        url = 'https://api.ipstack.com/' + ip_address + '?access_key=5dd2d3da467259fc47a71a6507825165'
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response['data'])
        getcontext().prec = 7
        latitude = Decimal(data['latitude'])
        longitude = Decimal(data['longitude'])
        services = ServiceDocument.filter("geo_distance", coordinates={"lat": latitude, "lon": longitude}, distance='1km')

    if ServiceRateDocument.search().count() > 0:
        service_rates = ServiceRateDocument.search().query(
            reduce(operator.ior, [
                Q(
                    'nested',
                    path='service',
                    query=Q('match', service__uuid=service.uuid),
                )
                for service in services
            ])
        ).sort('-created_at')
    else:
        service_rates = []

    service_rates_mapping = []
    service_rate_totals_mapping = {}
    service_rate_counts = []
    average_mapping = []
    for service in services:
        for service_rate in service_rates:
            if service_rate.service.uuid == service.uuid:
                service_rates_mapping.append((service.uuid, service_rate))
                service_rate_counts.append(service_rate.service.uuid)
                if service.uuid not in service_rate_totals_mapping.keys():
                    service_rate_totals_mapping[service.uuid] = service_rate.rate
                else:
                    service_rate_totals_mapping[service.uuid] += service_rate.rate

    for service in services:
        service_rate_count = len(list(filter(lambda s: service.uuid == s, service_rate_counts)))
        if service.uuid in service_rate_totals_mapping.keys():
            average_mapping = service.uuid, service_rate_totals_mapping[service.uuid] / service_rate_count

    return render(request, 'default.html', {
        'services': services,
        'service_rates': service_rates,
        'service_rates_mapping': service_rates_mapping,
        'average_mapping': average_mapping,
    })
