from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/', views.show, name='members.show'),
    path('home/', views.home, name='members.home'),
    path('register/', views.Register.as_view(), name='members.register'),
    path('login/', views.LoginView.as_view(), name='members.login'),
]
