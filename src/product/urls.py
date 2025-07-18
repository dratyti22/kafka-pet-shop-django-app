from django.urls import path

from src.product.views import CategoryView

app_name = "product"

urlpatterns = [

    path("category/", CategoryView.as_view(), name="get_category"),
    path("category/<str:slug>", CategoryView.as_view(), name="get_category"),

]
