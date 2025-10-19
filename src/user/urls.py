from django.urls import path
from rest_framework.routers import SimpleRouter

from src.user.views import (
                  UserActivateView,
                  UserLoginView,
                  UserProfileView,
                  UserRegisterView,
                  user_logout_view,
)

app_name = "user"
route = SimpleRouter()
route.register("profile/me", viewset=UserProfileView, basename="profile-me")

urlpatterns = [
                  path("register", UserRegisterView.as_view(), name="register"),
                  path("activate/<str:token>", UserActivateView.as_view(), name="activate"),
                  path("login", UserLoginView.as_view(), name="login"),
                  path("logout/", user_logout_view, name="logout"),
              ] + route.urls
