from django.urls import path

from src.user.views import UserActivateView, UserRegisterView

app_name = "user"

urlpatterns = [
    path("register", UserRegisterView.as_view(), name="register"),
    path("activate/<str:uidb64>/<str:token>", UserActivateView.as_view(), name="activate"),
]
