from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='activities.index'),
    path('attend/', views.attend_to_activity, name='activities.attend'),
    path('cancel/', views.cancel_activity_attendance, name='activities.cancel_attendance'),
    path('<uuid:pk>/attendants/', views.activity_attendants, name='activities.attendants'),
    path('search/', views.ActivityDocumentView.as_view({'get': 'list'}), name='activities.search'),
    path('new/', views.ActivityCreateView.as_view(), name='activities.create'),
    path('<uuid:pk>/edit/', views.ActivityUpdateView.as_view(), name='activities.update'),
    path('<uuid:pk>/', views.activity_detail, name='activities.detail'),
    path('rate/', views.rate, name='activities.rate'),
]
