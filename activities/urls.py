from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='activities.index'),
    path('<uuid:pk>/', views.show, name='activities.show'),
    path('search/', views.ActivityDocumentView.as_view({'get': 'list'}), name='activities.search'),
    path('new/', views.ActivityCreateView.as_view(), name='activities.create'),
    path('<uuid:pk>/edit/', views.ActivityUpdateView.as_view(), name='activities.update'),
]
