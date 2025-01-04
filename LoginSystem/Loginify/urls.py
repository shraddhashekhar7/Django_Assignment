from django.urls import path
from . import views

urlpatterns = [
    path("", views.hello_world, name="hello_world"),
    path("signup/", views.sign_up, name="sign_up"),
    path("login/", views.login, name="login"),
    path("all_data/", views.all_data, name="all_data"),
    path("single-user-data/<str:email>/",views.single_user_data, name="single_user_data"),
]