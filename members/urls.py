from django.urls import path

from . import views

urlpatterns = [
    path('<uuid:member_id>/', views.show, name='members.show'),
    path('home/', views.home, name='members.home'),
    path('signup/', views.SignUp.as_view(), name='members.signup'),
]
