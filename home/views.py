from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET


@require_GET
@login_required
def feed(request):
    return render(request, 'default.html')
