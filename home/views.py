import operator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from services.documents import ServiceDocument, ServiceRateDocument
from elasticsearch_dsl.query import Q
from functools import reduce


@require_GET
@login_required
def feed(request):
    context = {}
    if not request.GET.get('nearby'):
        services = ServiceDocument.search().sort('-start_date')
    else:
        services = []

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
