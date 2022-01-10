import json
import operator

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from activities.models import Activity, ActivityRate, ActivityAttendance, ActivityAttendanceRequest
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from activities.forms import ActivityCreateForm, ActivityUpdateForm
from activities.viewsets import ActivityDocumentViewSet
from activities.serializers import ActivityDocumentSerializer
from django.contrib.auth.decorators import login_required
from members.models import Member
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from elasticsearch_dsl.query import Q
from functools import reduce
from activities.documents import (
    ActivityDocument,
    ActivityAttendanceDocument,
    ActivityRateDocument,
    ActivityAttendanceRequestDocument
)


@require_GET
def index(request) -> HttpResponse:
    return HttpResponse('Hello world!')


@method_decorator(never_cache, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ActivityCreateView(LoginRequiredMixin, CreateView):
    form_class = ActivityCreateForm
    template_name = 'activities/activity_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user

        if form.instance.owner != self.request.user:
            return super(ActivityCreateView, self).form_invalid(form)
        return super().form_valid(form)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@method_decorator(never_cache, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
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

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@never_cache
@login_required
def activity_detail(request, pk):
    try:
        activity_search = ActivityDocument.search().filter('match_phrase', uuid=pk)
        activity = next(activity_search.__iter__())
        all_attendance = ActivityAttendanceDocument.search().filter(
            'nested',
            path='activity',
            query=Q(
                'match',
                activity__uuid=pk,
            ),
        )

        attendance_search = ActivityAttendanceDocument.search().query(
            reduce(
                operator.iand,
                [
                    Q(
                        'nested',
                        path='member',
                        query=Q('match', member__id=request.user.pk),
                    ),
                    Q(
                        'nested',
                        path='activity',
                        query=Q('match', activity__uuid=activity.uuid),
                    ),
                ]
            ),
        ).sort('-created_at')

        if attendance_search.count() > 0:
            member_status_on_event = 'can_cancel_attendance'
        else:
            member_status_on_event = 'can_attend'

        event_rates = ActivityRateDocument.search().filter(
            'nested',
            path='activity',
            query=Q('match', activity__uuid=activity.uuid)
        )

        if event_rates.count() > 0:
            average = sum(map(lambda event_rate: event_rate.rate, event_rates)) / event_rates.count()
            member_rates = [event_rate for event_rate in event_rates if event_rate.voter.id == request.user.pk]
            member_rated = len(member_rates) > 0
        else:
            average = 0
            member_rated = False

    except Activity.DoesNotExist:
        raise Activity.DoesNotExist('Event does not exist')

    return render(request, 'activities/activity_detail.html', {
        'event': activity,
        'average': '{:.2f}'.format(average),
        'member_status_on_event': member_status_on_event,
        'event_rates': event_rates,
        'positive_overall_iterator': range(round(average)),
        'negative_overall_iterator': range(round(average), 5),
        'member_rate_iterator': range(1, 6),
        'member_rated': member_rated,
        'all_attendance': all_attendance,
    })


@never_cache
@login_required
def attend_to_activity(request):
    request_data = json.loads(request.body)
    activity = Activity.objects.get(pk=request_data['event_id'])
    activity_attendance = ActivityAttendance(
        member=request.user,
        activity=activity,
        owner=activity.owner,
    )

    activity_attendance.save()
    status = 'approved'

    return JsonResponse({
        'status': status,
    })


@never_cache
@login_required
def cancel_activity_attendance(request):
    request_data = json.loads(request.body)
    activity = Activity.objects.get(pk=request_data['event_id'])
    activity_attendance = ActivityAttendance.objects.get(
        activiy=activity.uuid,
        member=request.user,
        owner=activity.owner,
    )

    activity_attendance.delete()
    status = 'approved'

    return JsonResponse({
        'status': status,
    })


@never_cache
@login_required
def activity_attendants(request, pk):
    activity_search = ActivityDocument.search().filter('match_phrase', uuid=pk)
    activity = next(activity_search.__iter__())
    all_attendance = ActivityAttendanceDocument.search().filter(
        'nested',
        path='activity',
        query=Q(
            'match',
            activity__uuid=pk,
        ),
    )

    return render(request, 'activities/activity_attendants.html', {
        'activity': activity,
        'all_attendance': all_attendance,
    })


@never_cache
@login_required
def rate(request):
    request_data = json.loads(request.body)
    activity = Activity.objects.get(pk=request_data['event_id'])
    member = Member.objects.get(pk=request.user.pk)
    activity_rate = ActivityRate(
        activity=activity,
        voter=member,
        rate=request_data['rate'],
        content=request_data['content'],
    )

    activity_rate.save()

    return JsonResponse({'status': 'success'})


class ActivityDocumentView(ActivityDocumentViewSet):
    document = ActivityDocument
    serializer_class = ActivityDocumentSerializer
