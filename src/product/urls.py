from django.urls import path
from rest_framework.routers import SimpleRouter

from src.product.views import AttributeProductView, CategoryView, PhotoProductView, ProductView

app_name = "product"

route = SimpleRouter()
route.register("", ProductView, basename="product")

urlpatterns = [

                  path("photo/", PhotoProductView.as_view({'get': 'list', 'post': 'create'}),
                       name="photo-list"),
                  path("photo/<int:pk>/", PhotoProductView.as_view(
                      {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
                       name="photo-detail"),
                  path("<str:product_slug>/photo/",
                       PhotoProductView.as_view({'get': 'list', 'post': 'create'}),
                       name="product-photo-list"),

                  path("attribute/", AttributeProductView.as_view({"get": "list", "post": "create"}),
                       name="attribute-list"),
                  path("attribute/<int:pk>/", AttributeProductView.as_view(
                      {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
                       name="attribute-detail"),
                  path("attribute/<str:product_slug>/", AttributeProductView.as_view(
                      {"get": "list", "post": "create"}
                  ),
                       name="attribute-product-list"),

                  path("category/", CategoryView.as_view(), name="get_category"),
                  path("category/<str:slug>", CategoryView.as_view(), name="get_category_one"),
              ] + route.urls
