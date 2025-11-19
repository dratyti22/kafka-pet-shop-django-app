from pickle import FALSE

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.cart.models import CartModel, OrderModel
from src.cart.pagination import CartPagination
from src.cart.serializers import CartSerializer
from src.cart.service import OrderService


class CartView(viewsets.GenericViewSet, CreateModelMixin, ListModelMixin,
               UpdateModelMixin, DestroyModelMixin):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CartPagination
    lookup_url_kwarg = "id"

    def get_queryset(self):
        from django.db.models import OuterRef, Prefetch, Subquery

        from src.product.models import PhotoProductModel, ProductModel

        main_photo = PhotoProductModel.objects.filter(
            product=OuterRef("pk"),
            is_main=True
        ).values("image")[:1]

        products_with_photo = ProductModel.objects.annotate(
            main_photo=Subquery(main_photo)
        )

        return CartModel.objects.filter(
            user=self.request.user
        ).prefetch_related(
            Prefetch('product', queryset=products_with_photo)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["POST"], detail=False, url_path="checkout")
    def checkout(self, request):
        cart_items_ids = request.data.get("cart_items", [])
        if not cart_items_ids:
            return Response({"error": "No cart items provided"}, status=status.HTTP_400_BAD_REQUEST)
        order = OrderService.checkout(request.user, cart_items_ids)
        return Response({"order_id": order.id, "status": order.status}, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=True, url_path="status")
    def status(self, request, pk=None):
        order = get_object_or_404(OrderModel, id=pk, user=request.user)
        return Response({"order_id": order.pk,"order_status":order.status,  "order_url_payment": order.url})

