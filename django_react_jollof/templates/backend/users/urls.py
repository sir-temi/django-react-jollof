from django.urls import include, path
from users.views import (
    RegisterView,
    LoginView,
    ProfileView,
    AdminOnlyView,
    UserOnlyView,
)

urlpatterns = [
    path("auth/", include("allauth.urls")),  # Include allauth's default URLs
    path("admin/", AdminOnlyView.as_view(), name="admin-only"),
    path("user/", UserOnlyView.as_view(), name="user-only"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
