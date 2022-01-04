import uuid

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.urls import reverse_lazy
from members.forms import RegisterForm, LoginForm
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import authenticate, login


@require_GET
def show(request, member_id: uuid.UUID) -> HttpResponse:
    return HttpResponse(f'This is the id of request {member_id.bytes}')


@require_GET
def home(request):
    return render(request, 'members/home.html')


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'registration/login.html'

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
                return redirect(reverse_lazy('members.home'))

        return super(LoginView, self).form_invalid(form)


class Register(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('members.login')
    template_name = 'registration/register.html'
