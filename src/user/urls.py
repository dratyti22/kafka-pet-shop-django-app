from django.urls import path

from src.user.views import UserActivateView, UserLoginView, UserRegisterView, user_logout_view

app_name = "user"

urlpatterns = [
    path("register", UserRegisterView.as_view(), name="register"),
    path("activate/<str:uidb64>/<str:token>", UserActivateView.as_view(), name="activate"),
    path("login", UserLoginView.as_view(), name="login"),
    path("logout/", user_logout_view, name="logout"),
]
