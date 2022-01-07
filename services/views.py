import json
from django.shortcuts import render
from django.http import HttpResponseNotFound, JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from services.models import Service, ServiceRate, ServiceAttendance, ServiceAttendanceRequest
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from services.forms import ServiceCreateForm, ServiceUpdateForm
from services.viewsets import ServiceDocumentViewSet
from services.documents import ServiceDocument
from services.serializers import ServiceDocumentSerializer
from django.contrib.auth.decorators import login_required
from members.models import Member
from django.views.decorators.cache import never_cache


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


# authentication required
def service_detail(request, pk):
    try:
        services = ServiceDocument.search().filter('match_phrase', uuid=pk)
    except Service.DoesNotExist:
        raise Service.DoesNotExist('Poll does not exist')

    return render(request, 'services/service_detail.html', {'services': services})


@never_cache
@login_required
def attend_to_service(request):
    request_data = json.loads(request.body)
    service = Service.objects.get(pk=request_data['service_id'])
    status = None
    member = Member.objects.get(pk=request.user.pk)

    if service.participant_picking == 2:
        service_attendance_request = ServiceAttendanceRequest(
            member=request.user,
            service=service,
            owner=service.owner,
        )
        service_attendance_request.save()
        status = 'waiting'

    elif service.participant_picking == 1:
        service_attendance = ServiceAttendance(
            member=request.user,
            service=service,
            owner=service.owner,
        )

        service_attendance.member.credit -= service.credit
        service_attendance.save()
        member = Member.objects.get(pk=request.user.pk)
        member.credit -= service.credit
        member.save()
        status = 'approved'
    else:
        raise Exception

    return JsonResponse({
        'status': status,
        'credit': member.credit,
    })


class ServiceDocumentView(ServiceDocumentViewSet):
    document = ServiceDocument
    serializer_class = ServiceDocumentSerializer

