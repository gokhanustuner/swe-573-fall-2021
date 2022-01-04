from django.urls import path

from . import views

urlpatterns = [
    path('<uuid:pk>/', views.ServiceDetailView.as_view(), name='services.detail'),
    path('new/', views.ServiceCreateView.as_view(), name='services.create'),
    path('<uuid:pk>/edit/', views.ServiceUpdateView.as_view(), name='services.update'),
    path('<uuid:pk>/delete/', views.ServiceDeleteView.as_view(), name='services.delete'),
    # path('delete/', views.delete, name='services.delete'),
]
