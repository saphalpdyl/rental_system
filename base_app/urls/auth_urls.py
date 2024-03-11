from django.urls import path

from base_app.views.auth import (
    LoginView,
    RegisterView,
    HandleLogout
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", HandleLogout.as_view(), name="logout"),
]
