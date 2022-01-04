from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from services.models import Service, ServiceRate, ServiceAttendance, ServiceAttendanceRequest
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from services.forms import ServiceCreateForm


class ServiceListView(ListView):
    pass


@method_decorator(never_cache, name='dispatch')
class ServiceCreateView(LoginRequiredMixin, CreateView):
    form_class = ServiceCreateForm
    template_name = 'services/service_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user

        if form.instance.owner != self.request.user:
            return super(ServiceCreateView, self).form_invalid(form)
        return super().form_valid(form)


@method_decorator(never_cache, name='dispatch')
class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    fields = [
        'title',
        'description',
        'location',
        'start_date',
        'end_date',
        'repetition_term',
        'privacy_status',
        'participant_limit',
        'participant_picking',
        'content',
        'cancelled',
    ]

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


class ServiceDetailView(DetailView):
    model = Service
