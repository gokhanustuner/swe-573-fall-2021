from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/edit/', views.MemberProfileUpdateView.as_view(), name='members.update'),
    path('<int:pk>/', views.show, name='members.show'),
    path('<int:pk>/settings/services/', views.services, name='members.services'),
    path('<int:pk>/settings/', views.settings, name='members.settings'),
    path('home/', views.home, name='members.home'),
    path('follow/', views.follow, name='members.follow'),
    path('unfollow/', views.unfollow, name='members.unfollow'),
    path('register/', views.RegisterView.as_view(), name='members.register'),
    path('login/', views.LoginView.as_view(), name='members.login'),
]
