from django.urls import path

from . import views

urlpatterns = [
    path('<uuid:pk>/', views.service_detail, name='services.detail'),
    path('<uuid:pk>/attendants/', views.service_attendants, name='services.attendants'),
    path('new/', views.ServiceCreateView.as_view(), name='services.create'),
    path('<uuid:pk>/edit/', views.ServiceUpdateView.as_view(), name='services.update'),
    path('<uuid:pk>/delete/', views.ServiceDeleteView.as_view(), name='services.delete'),
    path('search/', views.ServiceDocumentView.as_view({'get': 'list'}), name='services.search'),
    path('attend/', views.attend_to_service, name='services.attend'),
    path('cancel/', views.cancel_service_attendance, name='services.cancel_attendance'),
    path('rate/', views.rate, name='services.rate'),
    # path('delete/', views.delete, name='services.delete'),
]
