import random
import operator
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.urls import reverse_lazy
from members.forms import RegisterForm, LoginForm, MemberProfileUpdateForm
from members.models import Member, MemberProfile, SocialDirectedGraph
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from elasticsearch_dsl.query import Q
from services.documents import ServiceDocument, ServiceAttendanceDocument, ServiceRateDocument
from activities.documents import ActivityDocument, ActivityAttendanceDocument, ActivityRateDocument
from functools import reduce
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator


@require_GET
@never_cache
@login_required
def show(request, pk):
    member = Member.objects.get(pk=pk)
    services = ServiceDocument.search().filter(
        'nested',
        path='owner',
        query=Q('match', owner__id=member.pk)
    ).sort('-created_at')

    events = ActivityDocument.search().filter(
        'nested',
        path='owner',
        query=Q('match', owner__id=member.pk)
    ).sort('-created_at')

    service_items = sorted(services, key=lambda x: random.random())
    event_items = sorted(events, key=lambda x: random.random())
    items = sorted(service_items + event_items, key=lambda x: random.random())

    if services.count() > 0:
        service_rates = ServiceRateDocument.search().query(
            reduce(operator.ior, [
                Q(
                    'nested',
                    path='service',
                    query=Q('match', service__uuid=service.uuid),
                )
                for service in services
            ])
        ).sort('-created_at')
    else:
        service_rates = []

    if events.count() > 0:
        event_rates = ActivityRateDocument.search().query(
            reduce(operator.ior, [
                Q(
                    'nested',
                    path='activity',
                    query=Q('match', activity__uuid=event.uuid),
                )
                for event in events
            ])
        ).sort('-created_at')
    else:
        event_rates = []

    service_rates = sorted(service_rates, key=lambda x: random.random())
    event_rates = sorted(event_rates, key=lambda x: random.random())
    item_rates = service_rates + event_rates
    item_rates_mapping = []
    item_rate_totals_mapping = {}
    item_rate_counts = []
    average_mapping = []
    item_rate_counts_mapping = []
    for item in items:
        for item_rate in item_rates:
            if item_rate.meta['index'] == 'service_rates':
                if item_rate.service.uuid == item.uuid:
                    item_rates_mapping.append((item.uuid, item_rate))
                    item_rate_counts.append(item_rate.service.uuid)
                    if item.uuid not in item_rate_totals_mapping.keys():
                        item_rate_totals_mapping[item.uuid] = item_rate.rate
                    else:
                        item_rate_totals_mapping[item.uuid] += item_rate.rate
            elif item.meta['index'] == 'activity_rates':
                if item_rate.activity.uuid == item.uuid:
                    item_rates_mapping.append((item.uuid, item_rate))
                    item_rate_counts.append(item_rate.activity.uuid)
                    if item.uuid not in item_rate_totals_mapping.keys():
                        item_rate_totals_mapping[item.uuid] = item_rate.rate
                    else:
                        item_rate_totals_mapping[item.uuid] += item_rate.rate

    for item in items:
        item_rate_count = len(list(filter(lambda i: item.uuid == i, item_rate_counts)))
        if item.uuid in item_rate_totals_mapping.keys():
            average_mapping.append((item.uuid, '{:.2f}'.format(item_rate_totals_mapping[item.uuid] / item_rate_count)))
            item_rate_counts_mapping.append((item.uuid, item_rate_count))

    connection = SocialDirectedGraph.objects.filter(source=request.user, target=member)
    followers = SocialDirectedGraph.objects.filter(target=member).count()
    following = SocialDirectedGraph.objects.filter(source=member).count()

    return render(request, 'members/member_detail.html', {
        'member': member,
        'services': services,
        'events': events,
        'items': items,
        'item_rates': item_rates,
        'item_rates_mapping': item_rates_mapping,
        'item_rate_counts_mapping': item_rate_counts_mapping,
        'average_mapping': average_mapping,
        'connection': connection,
        'followers': followers,
        'following': following,
    })


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


@method_decorator(never_cache, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class MemberProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MemberProfile
    form_class = MemberProfileUpdateForm
    template_name = 'members/member_edit.html'

    def form_valid(self, form):
        form.instance.member = self.request.user
        return super(MemberProfileUpdateView, self).form_valid(form)

    def get_object(self):
        obj, created = MemberProfile.objects.get_or_create(member=self.request.user)
        return obj

    def test_func(self):
        member_profile = self.get_object()
        return member_profile.member == self.request.user

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


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


@never_cache
@login_required
def follow(request):
    request_data = json.loads(request.body)
    target = Member.objects.get(pk=request_data['target_id'])
    graph = SocialDirectedGraph(
        source=request.user,
        target=target,
    )

    graph.save()

    return JsonResponse({'status': 'success'})


@never_cache
@login_required
def unfollow(request):
    request_data = json.loads(request.body)
    target = Member.objects.get(pk=request_data['target_id'])
    SocialDirectedGraph.objects.filter(
        source=request.user,
        target=target,
    ).delete()

    return JsonResponse({'status': 'success'})


def test_func(self):
    service = self.get_object()
    return service.owner == self.request.user