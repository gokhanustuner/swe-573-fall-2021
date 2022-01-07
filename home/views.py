from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from services.documents import ServiceDocument


@require_GET
@login_required
def feed(request):
    context = {}
    if not request.GET.get('nearby'):
        services = ServiceDocument.search().sort('-start_date')
    else:
        services = []
    return render(request, 'default.html', {
        'services': services,
    })
