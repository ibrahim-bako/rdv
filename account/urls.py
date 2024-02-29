from django.urls import path

from .views import (
    login,
    register,
    become_service_provider,
    logout,
)

urlpatterns = [
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout, name="logout"),
    path("become_service_provider/", become_service_provider, name="become_service_provider"),
]
