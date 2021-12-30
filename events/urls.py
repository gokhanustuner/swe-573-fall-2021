from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='events.index'),
    path('<uuid:event_id>/', views.show, name='events.show'),
]
