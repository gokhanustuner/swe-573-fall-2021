import operator
import socket
import requests
import random
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from services.documents import ServiceDocument, ServiceRateDocument
from activities.documents import ActivityDocument, ActivityRateDocument
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
        services = ServiceDocument.search().filter('match', delivered=True).sort('-start_date')
        events = ActivityDocument.search().sort('-start_date')

        service_items = sorted(services, key=lambda x: random.random())
        event_items = sorted(events, key=lambda x: random.random())
        items = sorted(service_items + event_items, key=lambda x: random.random())
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

    if services.count() > 0:
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

    if events.count() > 0:
        event_rates = ActivityRateDocument.search().query(
            reduce(operator.ior, [
                Q(
                    'nested',
                    path='activity',
                    query=Q('match', activity__uuid=event.uuid),
                )
                for event in events
            ])
        ).sort('-created_at')
    else:
        event_rates = []

    service_rates = sorted(service_rates, key=lambda x: random.random())
    event_rates = sorted(event_rates, key=lambda x: random.random())
    item_rates = service_rates + event_rates
    item_rates_mapping = []
    item_rate_totals_mapping = {}
    item_rate_counts = []
    average_mapping = []
    item_rate_counts_mapping = []
    for item in items:
        for item_rate in item_rates:
            if item_rate.meta['index'] == 'service_rates':
                if item_rate.service.uuid == item.uuid:
                    item_rates_mapping.append((item.uuid, item_rate))
                    item_rate_counts.append(item_rate.service.uuid)
                    if item.uuid not in item_rate_totals_mapping.keys():
                        item_rate_totals_mapping[item.uuid] = item_rate.rate
                    else:
                        item_rate_totals_mapping[item.uuid] += item_rate.rate
            elif item.meta['index'] == 'activity_rates':
                if item_rate.activity.uuid == item.uuid:
                    item_rates_mapping.append((item.uuid, item_rate))
                    item_rate_counts.append(item_rate.activity.uuid)
                    if item.uuid not in item_rate_totals_mapping.keys():
                        item_rate_totals_mapping[item.uuid] = item_rate.rate
                    else:
                        item_rate_totals_mapping[item.uuid] += item_rate.rate

    for item in items:
        item_rate_count = len(list(filter(lambda i: item.uuid == i, item_rate_counts)))
        if item.uuid in item_rate_totals_mapping.keys():
            average_mapping.append((item.uuid, '{:.2f}'.format(item_rate_totals_mapping[item.uuid] / item_rate_count)))
            item_rate_counts_mapping.append((item.uuid, item_rate_count))

    return render(request, 'default.html', {
        'items': items,
        'item_rates': item_rates,
        'item_rates_mapping': item_rates_mapping,
        'item_rate_counts_mapping': item_rate_counts_mapping,
        'average_mapping': average_mapping,
    })
