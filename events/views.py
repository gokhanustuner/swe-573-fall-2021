import uuid

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def index(request) -> HttpResponse:
    return HttpResponse('Hello world!')


@require_GET
@login_required
def show(request, event_id: uuid.UUID) -> HttpResponse:
    return HttpResponse(f'This is the id of request {event_id.bytes}')
