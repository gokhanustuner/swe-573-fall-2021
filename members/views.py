import uuid

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.urls import reverse_lazy
from members.forms import RegisterForm, LoginForm
from members.models import Member
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from elasticsearch_dsl.query import Q
from services.documents import ServiceDocument, ServiceAttendanceDocument


@require_GET
@never_cache
@login_required
def show(request, pk: int) -> HttpResponse:
    return HttpResponse(f'This is the id of request {pk}')


@require_GET
def home(request):
    return render(request, 'members/home.html')


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'members/login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or ''
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)

            if redirect_path != '':
                return redirect(redirect_path)
            else:
                return redirect(reverse_lazy('home.feed'))

        return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('members.login')
    template_name = 'members/register.html'


@never_cache
@login_required
def settings(request, pk):
    return render(request, 'members/settings.html')


def services(request, pk):
    service_list = ServiceDocument.search().filter(
        'nested',
        path='owner',
        query=Q(
            'match',
            owner__id=pk,
        ),
    )

    return render(request, 'members/services.html', {
        'services': service_list,
    })


def test_func(self):
    service = self.get_object()
    return service.owner == self.request.user