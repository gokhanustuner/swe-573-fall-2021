import uuid
import json
import operator

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from activities.models import Activity, ActivityRate, ActivityAttendance, ActivityAttendanceRequest
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from activities.forms import ActivityCreateForm, ActivityUpdateForm
from activities.viewsets import ActivityDocumentViewSet
from activities.documents import ActivityDocument, ActivityAttendanceDocument, ActivityAttendanceRequestDocument
from activities.serializers import ActivityDocumentSerializer
from django.contrib.auth.decorators import login_required
from members.models import Member
from django.views.decorators.cache import never_cache
from elasticsearch_dsl.query import Q
from functools import reduce


@require_GET
def index(request) -> HttpResponse:
    return HttpResponse('Hello world!')


@require_GET
@login_required
def show(request, event_id: uuid.UUID) -> HttpResponse:
    return HttpResponse(f'This is the id of request {event_id.bytes}')


@method_decorator(never_cache, name='dispatch')
class ActivityCreateView(LoginRequiredMixin, CreateView):
    form_class = ActivityCreateForm
    template_name = 'activities/activity_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user

        if form.instance.owner != self.request.user:
            return super(ActivityCreateView, self).form_invalid(form)
        return super().form_valid(form)


@method_decorator(never_cache, name='dispatch')
class ActivityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Activity
    form_class = ActivityUpdateForm
    template_name = 'activities/activity_edit.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        activity = self.get_object()
        return activity.owner == self.request.user


class ActivityDocumentView(ActivityDocumentViewSet):
    document = ActivityDocument
    serializer_class = ActivityDocumentSerializer
