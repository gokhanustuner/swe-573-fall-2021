from django.urls import path

from . import views

urlpatterns = [
    path('<uuid:service_id>/', views.show, name='services.show'),
    path('new/', views.new, name='services.new'),
    path('edit/<uuid:service_id>/', views.edit, name='services.edit'),
    path('create/', views.create, name='services.create'),
    path('update/', views.update, name='services.update'),
    # path('delete/', views.delete, name='services.delete'),
]
