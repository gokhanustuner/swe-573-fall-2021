import json
import operator

from django.shortcuts import render
from django.http import HttpResponseNotFound, JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from services.models import Service, ServiceRate, ServiceAttendance, ServiceAttendanceRequest
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from services.forms import ServiceCreateForm, ServiceUpdateForm
from services.viewsets import ServiceDocumentViewSet
from services.documents import ServiceDocument, ServiceAttendanceDocument, ServiceAttendanceRequestDocument
from services.serializers import ServiceDocumentSerializer
from django.contrib.auth.decorators import login_required
from members.models import Member
from django.views.decorators.cache import never_cache
from elasticsearch_dsl.query import Q
from functools import reduce


class ServiceListView(ListView):
    pass


@method_decorator(never_cache, name='dispatch')
class ServiceCreateView(LoginRequiredMixin, CreateView):
    form_class = ServiceCreateForm
    template_name = 'services/service_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user

        if form.instance.owner != self.request.user:
            return super(ServiceCreateView, self).form_invalid(form)
        return super().form_valid(form)


@method_decorator(never_cache, name='dispatch')
class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    form_class = ServiceUpdateForm
    template_name = 'services/service_edit.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        service = self.get_object()
        return service.owner == self.request.user


@method_decorator(never_cache, name='dispatch')
class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Service
    success_url = '/'

    def test_func(self):
        service = self.get_object()
        return service.owner == self.request.user


@never_cache
@login_required
def service_detail(request, pk):
    try:
        service_search = ServiceDocument.search().filter('match_phrase', uuid=pk)
        service = next(service_search.__iter__())
        member = Member.objects.get(pk=request.user.pk)
        all_attendance = ServiceAttendanceDocument.search().filter(
            'nested',
            path='service',
            query=Q(
                'match',
                service__uuid=pk,
            ),
        )

        attendance_search = ServiceAttendanceDocument.search().query(
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
                        path='service',
                        query=Q('match', service__uuid=service.uuid),
                    ),
                ]
            ),
        ).sort('-created_at')

        if not service.delivered or service.cancelled:
            if attendance_search.count() > 0:
                member_status_on_service = 'can_cancel_attendance'
            else:
                if (member.credit - service.credit) >= 0:
                    if service.participant_limit <= (service.participant_limit + 1):
                        member_status_on_service = 'can_attend'
                    else:
                        member_status_on_service = 'insufficient_limit'
                else:
                    member_status_on_service = 'insufficient_credit'
        else:
            if service.delivered:
                member_status_on_service = 'service_delivered'
            elif service.cancelled:
                member_status_on_service = 'service_cancelled'
    except Service.DoesNotExist:
        raise Service.DoesNotExist('Service does not exist')

    return render(request, 'services/service_detail.html', {
        'service': service,
        'member_status_on_service': member_status_on_service,
        'all_attendance': all_attendance,
    })


@never_cache
@login_required
def attend_to_service(request):
    request_data = json.loads(request.body)
    service = Service.objects.get(pk=request_data['service_id'])
    service_attendance = ServiceAttendance(
        member=request.user,
        service=service,
        owner=service.owner,
    )

    service_attendance.member.credit -= service.credit
    service_attendance.owner.credit += service.credit
    service_attendance.save()
    member = Member.objects.get(pk=request.user.pk)
    owner = Member.objects.get(pk=service_attendance.owner.pk)
    member.credit -= service.credit
    owner.credit += service.credit
    member.save()
    owner.save()
    status = 'approved'

    return JsonResponse({
        'status': status,
        'credit': service_attendance.member.credit,
    })


@never_cache
@login_required
def cancel_service_attendance(request):
    request_data = json.loads(request.body)
    service = Service.objects.get(pk=request_data['service_id'])
    member = Member.objects.get(pk=request.user.pk)
    service_attendance = ServiceAttendance.objects.get(
        service=service.uuid,
        member=member,
        owner=service.owner,
    )

    service_attendance.member.credit += service.credit
    service_attendance.save()
    member = Member.objects.get(pk=request.user.pk)
    owner = Member.objects.get(pk=service_attendance.owner.pk)
    member.credit += service.credit
    owner.credit -= service.credit
    member.save()
    owner.save()
    service_attendance.delete()
    status = 'approved'

    return JsonResponse({
        'status': status,
        'credit': member.credit,
    })


@never_cache
@login_required
def service_attendants(request, pk):
    service_search = ServiceDocument.search().filter('match_phrase', uuid=pk)
    service = next(service_search.__iter__())
    all_attendance = ServiceAttendanceDocument.search().filter(
        'nested',
        path='service',
        query=Q(
            'match',
            service__uuid=pk,
        ),
    )

    return render(request, 'services/service_attendants.html', {
        'service': service,
        'all_attendance': all_attendance,
    })


@never_cache
@login_required
def rate(request):
    request_data = json.loads(request.body)
    service = Service.objects.get(pk=request_data['service_id'])
    member = Member.objects.get(pk=request.user.pk)
    service_rate = ServiceRate(
        service=service,
        voter=member,
        rate=request_data['rate'],
        content=request_data['content'],
    )

    service_rate.save()

    return JsonResponse({'status': 'success'})


class ServiceDocumentView(ServiceDocumentViewSet):
    document = ServiceDocument
    serializer_class = ServiceDocumentSerializer

