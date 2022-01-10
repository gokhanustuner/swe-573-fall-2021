import json

from django.shortcuts import render
from services.documents import ServiceDocument
from activities.documents import ActivityDocument
from elasticsearch_dsl.query import Q
from django.http import JsonResponse
from elasticsearch_dsl import Search


def search(request):
    query = request.GET.get('search')
    services_matching_by_title = []
    services_matching_by_owners_full_name = []
    events_matching_by_title = []
    events_matching_by_owners_full_name = []
    services_matching_by_title_query_set = ServiceDocument.search().filter('match_phrase', title=query).sort('-created_at')
    services_matching_by_owners_full_name_query_set = ServiceDocument.search().filter(
        'nested',
        path='owner',
        query=Q('match_phrase', owner__full_name=query)
    ).sort('-created_at')
    events_matching_by_title_query_set = ActivityDocument.search().filter('match_phrase', title=query).sort('-created_at')
    events_matching_by_owners_full_name_query_set = ActivityDocument.search().filter(
        'nested',
        path='owner',
        query=Q('match_phrase', owner__full_name=query)
    ).sort('-created_at')

    for service_matching_by_title in services_matching_by_title_query_set:
        services_matching_by_title.append(service_matching_by_title.to_dict())

    for service_matching_by_owners_full_name in services_matching_by_owners_full_name_query_set:
        services_matching_by_owners_full_name.append(service_matching_by_owners_full_name.to_dict())

    for event_matching_by_title in events_matching_by_title_query_set:
        events_matching_by_title.append(event_matching_by_title.to_dict())

    for event_matching_by_owners_full_name in events_matching_by_owners_full_name_query_set:
        events_matching_by_owners_full_name.append(event_matching_by_owners_full_name.to_dict())

    return JsonResponse({
        'services_matching_by_title': services_matching_by_title,
        'services_matching_by_owners_full_name': services_matching_by_owners_full_name,
        'events_matching_by_title': events_matching_by_title,
        'events_matching_by_owners_full_name': events_matching_by_owners_full_name,
    })


