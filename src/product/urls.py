from django.urls import path
from rest_framework.routers import SimpleRouter

from src.product.views import CategoryView, ProductView

app_name = "product"

route = SimpleRouter()
route.register("", ProductView, basename="product")

urlpatterns = [
    *route.urls,

    path("category/", CategoryView.as_view(), name="get_category"),
    path("category/<str:slug>", CategoryView.as_view(), name="get_category_one"),

]
