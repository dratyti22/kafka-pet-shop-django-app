from rest_framework.routers import SimpleRouter

from src.cart.views import CartView

route = SimpleRouter()

route.register("", CartView, basename="cart")

urlpatterns = [

              ] + route.urls
