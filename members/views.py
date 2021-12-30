import uuid

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.urls import reverse_lazy
from members.admin import UserCreationForm
from django.views.generic.edit import CreateView


@require_GET
def show(request, member_id: uuid.UUID) -> HttpResponse:
    return HttpResponse(f'This is the id of request {member_id.bytes}')


@require_GET
def home(request):
    return render(request, 'members/home.html')


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
